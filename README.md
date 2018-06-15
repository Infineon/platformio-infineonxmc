# platformio-infineonxmc
Scripts and examples for developing XMC Microcontroller Boards using Platform IO

## Usage

The scripts in this repository is not yet in the official registry of Platform IO, to use it in your project (assuming you have installed Platform IO), you have to manually clone/unzip this repository under **C:\Users\UserName\.platformio\platforms\** and make sure the created folder is called **platformio-infineonxmc**

## Configuration for Debbuger

In order to use the Unified Debbuger from Platform IO to debug XMC boards, you need to modify the **platform.ini** file of your project. 

```
[env:xmc1100_xmc2go]
platform = infineonxmc
board = xmc1100_xmc2go
framework = arduino

; needed for debugging
debug_tool = custom
debug_server = 
    JLinkGDBServerCL
    -singlerun
    -if 
    SWD
    -select
    USB
    -port
    2331
    -device
    XMC1100-0064
```  

The `-device` option should be adapted for different boards:
* For all the supported XMC1100 boards: 
```
    -device
    XMC1100-0064
```

* For XMC1300 Boot Kit:
```
    -device
    XMC1300-0200
```

* For XMC1300 Sense2GoL:
```
    -device
    XMC1300-0032
```

* For XMC4200 Distance2Go (Upcoming):
```
    -device
    XMC4200-256
```

* For XMC4700 Relax Kit:
```
    -device
    XMC4700-2048
```