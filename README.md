# Infineon XMC: development platform for [PlatformIO](https://platformio.org)
[![Build Status](https://travis-ci.org/Infineon/platformio-infineonxmc.svg?branch=master)](https://travis-ci.org/Infineon/platformio-infineonxmc)
[![Build status](https://ci.appveyor.com/api/projects/status/wfs5ekp9tcntmdw5?svg=true)](https://ci.appveyor.com/project/sherylll/platformio-infineonxmc)

Infineon has designed the XMC microcontrollers for real-time critical applications with an industry-standard core. The XMC microcontrollers can be integrated with the Arduino platform

* [Home](https://registry.platformio.org/platforms/platformio/infineonxmc) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/infineonxmc.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
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

Please navigate to [documentation](https://docs.platformio.org/page/platforms/infineonxmc.html).
