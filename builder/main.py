# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import makedirs
from os.path import join, isdir
from platform import system

from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment


env = DefaultEnvironment()
platform = env.PioPlatform()

env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    GDB="arm-none-eabi-gdb",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-gcc-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ARFLAGS=["rcs"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARM.exidx)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGSUFFIX=".elf"
)

env.Append(
    ASFLAGS=[
        "-c",
        "-g",
        "-w",
        "-x", "assembler-with-cpp",
        "-mthumb"
    ],

    CFLAGS=[
        "-MMD"
    ],

    # both c and cpp
    CCFLAGS=[
        "-Os",  # optimize for size
        "-w",  # disables compiler warnings
        "-nostdlib",
        "-Wall",  # show warnings
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mthumb"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-threadsafe-statics",
        "-fpermissive",
        "-mthumb"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    LINKFLAGS=[
        "-Os",
        "-nostartfiles",
        "-nostdlib",
        "-Wl,--gc-sections",
        "-mthumb",
        "--specs=nano.specs",
        "--specs=nosys.specs"
    ],

    LIBS=["m", "gcc", "c", "stdc++"],

    BUILDERS=dict(
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

if "BOARD" in env:
    arm_math = "ARM_MATH_CM0"
    arm_dsp = ""
    usb0_used = ""
    if env.BoardConfig().get("build.variant")[-4] == '4':
        arm_math = "ARM_MATH_CM4"
        arm_dsp = "ARM_MATH_DSP"
        usb0_used = "USB0"
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ],
        CPPDEFINES=[
            env.BoardConfig().get("build.mcu"),
            arm_dsp,  # comment out if no DSP needed
            arm_math,
            usb0_used,
            "_INIT_DECLARATION_REQUIRED"
        ],
        LINKFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ]
    )

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.hex")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#
target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload firmware
#
debug_tools = env.BoardConfig().get("debug.tools", {})
upload_protocol = env.subst("$UPLOAD_PROTOCOL")


def _jlink_cmd_script(env, source):
    build_dir = env.subst("$BUILD_DIR")
    if not isdir(build_dir):
        makedirs(build_dir)
    script_path = join(build_dir, "upload.jlink")
    mcu = env.BoardConfig().get("build.mcu")
    commands = []
    if (mcu == "XMC1400" or mcu == "XMC1300" or mcu == "XMC1100"):
        commands = ["loadbin %s,0x10001000" % source, "r", "go", "exit"]
    elif (mcu == "XMC4700" or mcu == "XMC4800"):
        commands = ["loadbin %s,0x08000000" % source, "r", "g", "exit"]
    with open(script_path, "w") as fp:
        fp.write("\n".join(commands))
    return script_path

env.Replace(
    __jlink_cmd_script=_jlink_cmd_script,
    UPLOADER="JLink.exe" if system() == "Windows" else "JLinkExe",
    UPLOADERFLAGS=[
        "-device", env.BoardConfig().get("debug", {}).get("jlink_device"),
        "-speed", "4000",
        "-if", ("jtag" if upload_protocol == "jlink-jtag" else "swd"),
        "-autoconnect", "1"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS -CommanderScript "${__jlink_cmd_script(__env__, SOURCE)}"'
)

upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]
AlwaysBuild(env.Alias("upload", target_firm, upload_actions))

#
# Target: Define targets
#

Default([target_buildprog, target_size])
