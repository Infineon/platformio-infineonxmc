# Infineon XMC: development platform for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/Infineon/platformio-infineonxmc/workflows/Examples/badge.svg)](https://github.com/Infineon/platformio-infineonxmc/actions)
[![Check links](https://github.com/Infineon/platformio-infineonxmc/actions/workflows/check_links.yml/badge.svg)](https://github.com/Infineon/platformio-infineonxmc/actions/workflows/check_links.yml)

Infineon has designed the XMC microcontrollers for real-time critical applications with an industry-standard core. The XMC microcontrollers can be integrated with the Arduino platform

* [Home](https://registry.platformio.org/platforms/infineon/infineonxmc) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/en/latest/projectconf/section_env_platform.html#platform) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = infineonxmc
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/Infineon/platformio-infineonxmc.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://registry.platformio.org/platforms/infineon/infineonxmc).
