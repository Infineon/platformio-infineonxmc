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

import sys

from platformio.public import PlatformBase


IS_WINDOWS = sys.platform.startswith("win")

class InfineonxmcPlatform(PlatformBase):

    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug['tools'] = {}

        # J-Link Probe
        link = "jlink"
        assert debug.get("jlink_device"), (
            "Missed J-Link Device ID for %s" % board.id)
        debug['tools'][link] = {
            "server": {
                "package": "tool-jlink",
                "arguments": [
                    "-singlerun",
                    "-if", "SWD",
                    "-select", "USB",
                    "-device", debug.get("jlink_device"),
                    "-port", "2331"
                ],
                "executable": ("JLinkGDBServerCL.exe"
                               if IS_WINDOWS else
                               "JLinkGDBServer")
            },
            "onboard": link in debug.get("onboard_tools", [])
        }
        board.manifest['debug'] = debug
        return board
