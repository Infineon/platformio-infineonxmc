# platformio-infineonxmc

[![Build Status](https://travis-ci.org/Infineon/platformio-infineonxmc.svg?branch=master)](https://travis-ci.org/Infineon/platformio-infineonxmc)

Scripts and examples for developing XMC Microcontroller Boards using Platform IO

## Usage

```
platformio platform install https://github.com/Infineon/platformio-infineonxmc.git
```

## Issue with XMC1300 Sense2GoL
There is likely a bug in the upload configuration for the Sense2GoL board. To flash this board please use XMC Flasher instead of the upload command in PlatformIO.