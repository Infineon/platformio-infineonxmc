from platformio.managers.platform import PlatformBase


class InfineonxmcPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        #if not variables.get("pioframework"):
        #    self.packages['sdk-esp8266']['optional'] = False
        #if "buildfs" in targets:
        #    self.packages['tool-mkspiffs']['optional'] = False
        return PlatformBase.configure_default_packages(self, variables, targets)