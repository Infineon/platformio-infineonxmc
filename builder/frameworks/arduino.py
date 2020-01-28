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

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment


env = DefaultEnvironment()
platform = env.PioPlatform()
board_config = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoxmc")
assert isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=[
        "ARDUINO_ARCH_ARM",
        ("ARDUINO", 10805)
    ],

    CFLAGS=[
        "-std=gnu11"
    ],

    CXXFLAGS=[
        "-std=gnu++11"
    ],

    LINKFLAGS=[
        "-T", env.BoardConfig().get("build.ldscript", join(
            platform.get_package_dir("framework-arduinoxmc"),
            "variants", env.BoardConfig().get("build.mcu"), "linker_script.ld")
        )
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "NN", "Include"),  # comment out if no NN needed
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "DSP", "Include"),  # comment out if no DSP needed
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "Include"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "LIBS"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "XMCLib", "inc"),
        join(FRAMEWORK_DIR, "cores", "usblib"),
        join(FRAMEWORK_DIR, "cores", "usblib","Class"),
        join(FRAMEWORK_DIR, "cores", "usblib","Class","Device"),
        join(FRAMEWORK_DIR, "cores", "usblib","Common"),
        join(FRAMEWORK_DIR, "cores", "usblib","Core"),
        join(FRAMEWORK_DIR, "cores", "usblib","Core","XMC4000"),
        join(FRAMEWORK_DIR, "cores", "avr"),
        join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"),
             "config", board_config.get("build.board_variant"))
    ],
)

env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores")
))
env.Prepend(LIBS=libs)
