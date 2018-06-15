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

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoxmc")
assert isdir(FRAMEWORK_DIR)

# USB flags
ARDUINO_USBDEFINES = [
    "ARDUINO_ARCH_ARM",
    ("ARDUINO", 10805)
]

env.Append(
    CPPDEFINES=ARDUINO_USBDEFINES,
    CFLAGS=[
        "-std=gnu11"
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "cores"),
#        join(FRAMEWORK_DIR,"cores","xmc_lib","CMSIS","DSP","include"), # comment out if no DSP needed
        join(FRAMEWORK_DIR,"cores","xmc_lib","CMSIS","include"),
        join(FRAMEWORK_DIR,"cores","xmc_lib","LIBS"),
        join(FRAMEWORK_DIR,"cores","xmc_lib","XMCLib","inc"),
        join(FRAMEWORK_DIR, "cores","avr"),        
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.family"),"config",env.BoardConfig().get("build.board_variant"))
    ],
    
    CXXFLAGS=[
        "-std=gnu++11"
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
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.family"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.family"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores")
    ))
env.Prepend(LIBS=libs)
