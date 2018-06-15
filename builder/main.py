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

from os.path import join
from time import sleep

from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, AlwaysBuild,
                          Builder, Default, DefaultEnvironment)

from platformio.util import get_serialports



env = DefaultEnvironment()
platform = env.PioPlatform()

def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621

    if "program" in COMMAND_LINE_TARGETS:
        return

    # if "micronucleus" in env['UPLOADER']:
        # print "Please unplug/plug device ..."

    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    # Deprecated: compatibility with old projects. Use `program` instead
    if "usb" in env.subst("$UPLOAD_PROTOCOL"):
        upload_options['require_upload_port'] = False
        env.Replace(UPLOAD_SPEED=None)

    if env.subst("$UPLOAD_SPEED"):
        env.Append(UPLOADERFLAGS=["-b", "$UPLOAD_SPEED"])

    # extra upload flags
    if "extra_flags" in upload_options:
        env.Append(UPLOADERFLAGS=upload_options.get("extra_flags"))

    # disable erasing by default
    env.Append(UPLOADERFLAGS=["-D"])

    if upload_options and not upload_options.get("require_upload_port", False):
        return

    env.AutodetectUploadPort()
    env.Append(UPLOADERFLAGS=["-P", '"$UPLOAD_PORT"'])

    if env.subst("$BOARD") in ("raspduino", "emonpi", "sleepypi"):

        def _rpi_sysgpio(path, value):
            with open(path, "w") as f:
                f.write(str(value))

        if env.subst("$BOARD") == "raspduino":
            pin_num = 18
        elif env.subst("$BOARD") == "sleepypi":
            pin_num = 22
        else:
            pin_num = 4

        _rpi_sysgpio("/sys/class/gpio/export", pin_num)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/direction" % pin_num, "out")
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 1)
        sleep(0.1)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 0)
        _rpi_sysgpio("/sys/class/gpio/unexport", pin_num)
    else:
        if not upload_options.get("disable_flushing", False) \
            and not env.get("UPLOAD_PORT", "").startswith("net:"):
            env.FlushSerialBuffer("$UPLOAD_PORT")

        before_ports = get_serialports()

        if upload_options.get("use_1200bps_touch", False):
            env.TouchSerialPort("$UPLOAD_PORT", 1200)

        if upload_options.get("wait_for_upload_port", False):
            env.Replace(UPLOAD_PORT=env.WaitForNewSerialPort(before_ports))
           
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

    ASFLAGS=["-c","-g","-w","-x", "assembler-with-cpp","-mthumb"],

    CFLAGS=[
        "-MMD"
    ],
    
    # both c and cpp
    CCFLAGS=[
        "-Os",  # optimize for size
        "-c",
        "-g",
        "-w", #disables compiler warnings
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

    CPPDEFINES=[("F_CPU", "$BOARD_F_CPU")],

    LINKFLAGS=[
        "-Os",
        "-nostartfiles",
        "-nostdlib",
        "-Wl,--gc-sections",
        "-mthumb",
        "--specs=nano.specs",
        "--specs=nosys.specs",
        "-Wl,-Map,"+join("$BUILD_DIR", "hi")+".map"
    ],

    LIBS=["m","gcc","c","stdc++"],
    
    PROGSUFFIX=".elf",
    
    FRAMEWORK_ARDUINOXMC_DIR=platform.get_package_dir(
        "framework-arduinoxmc"),
)

if "BOARD" in env:
    arm_math = "ARM_MATH_CM0"
    if "ARM_MATH_CM"+env.BoardConfig().get("build.variant")[-4] == 4:
        arm_math = "ARM_MATH_CM4"
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ],
        CPPDEFINES=[
            env.BoardConfig().get("build.family"),
#            "ARM_MATH_DSP", # comment out if no DSP needed
            arm_math,
            "_INIT_DECLARATION_REQUIRED"
        ],
        LINKFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
            "-T"+join(platform.get_package_dir("framework-arduinoxmc"),"variants",env.BoardConfig().get("build.family"),"linker_script.ld")
        ]
)
     
env.Append(
    CPPPATH = [
    ],
    
    ASFLAGS=env.get("CCFLAGS", [])[:],
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

#print env.subst('$OBJCOPY')

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildProgram()

#
# Target: Print binary size
#
target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Build the .hex file
#
target_hex = env.ElfToHex(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Upload firmware
#
upload = env.Alias(["upload"], target_hex, "$UPLOADCMD")
AlwaysBuild(upload)


variant = env.BoardConfig().get("build.variant")
v = env.BoardConfig().get("build.v")
env.Replace(
    UPLOADER= join(platform.get_package_dir("tool-xmcflasher"),"XMCFlasher.jar"),
    UPLOADCMD = "java -jar $UPLOADER -p $BUILD_DIR/firmware.hex -device " + variant +"-" + v
)

#
# Target: Define targets
#
Default([target_hex,target_size])