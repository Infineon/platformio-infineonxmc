from platformio.managers.platform import PlatformBase
from platform import system

class InfineonxmcPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        return PlatformBase.configure_default_packages(self, variables, targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result
        
    def _add_default_debug_tools(self, board):
        print board
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug['tools'] = {}

        # J-Link Probe
        link = "jlink"
        assert debug.get("jlink_device"), (
            "Missed J-Link Device ID for %s" % board.id)
        debug['tools'][link] = {
            "server": {
                "arguments": [
                    "-singlerun",
                    "-if", "SWD",
                    "-select", "USB",
                    "-device", debug.get("jlink_device"),
                    "-port", "2331"
                ],
                "executable": ("JLinkGDBServerCL.exe"
                               if system() == "Windows" else
                               "JLinkGDBServer")
            },
            "onboard": link in debug.get("onboard_tools", [])
        }
        board.manifest['debug'] = debug
        return board    