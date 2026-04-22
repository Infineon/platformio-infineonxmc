# Infineon XMC: development platform for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/Infineon/platformio-infineonxmc/workflows/Examples/badge.svg)](https://github.com/Infineon/platformio-infineonxmc/actions)

Infineon has designed the XMC microcontrollers for real-time critical applications with an industry-standard core. The XMC microcontrollers can be integrated with the Arduino platform.

## Quick Start

1. [Install PlatformIO](https://platformio.org)
2. Create a new PlatformIO project
3. In the generated `platformio.ini`, set `platform`, `framework`, and `board`:

```ini
[env:myproject]
platform = https://github.com/Infineon/platformio-infineonxmc.git
framework = arduino
board = ...
```

## Supported Boards

| Board | `board` value |
|---|---|
| XMC1100 Boot Kit | `kit_xmc11_boot_001` |
| XMC1100 XMC2Go | `kit_xmc_2go_xmc1100_v1` |
| XMC1300 Boot Kit | `kit_xmc13_boot_001` |
| XMC1400 Arduino | `kit_xmc1400_arduino` |
| XMC1400 XMC2Go | `kit_xmc14_2go` |
| XMC4700 Relax Kit | `kit_xmc47_relax` |

## Updating the Framework Version

The framework version is pinned in `platform.json` as a Release ZIP. To update, change the ZIP URL to the new version:

```json
"version": "https://github.com/Infineon/XMC-for-Arduino/releases/download/X.Y.Z/xmc-for-arduino-X.Y.Z.zip"
```

Available releases: https://github.com/Infineon/XMC-for-Arduino/releases

Alternatively, you can point directly to the latest git master:

```json
"version": "https://github.com/Infineon/XMC-for-Arduino.git"
```

> **Note:** Using git master means `cores/xmc/api/` will be empty because it is a git submodule that PlatformIO does not populate automatically. You must fix it manually after install:
> ```bash
> cd ~/.platformio/packages/framework-arduinoxmc
> git submodule update --init --recursive
> ```
