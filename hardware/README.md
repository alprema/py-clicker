
# Hardware

## Overview

[<img src="clicker_front.jpg" alt="drawing" width="300"/>](clicker_front.jpg)
[<img src="clicker_back.jpg" alt="drawing" width="300"/>](clicker_back.jpg)
[<img src="clicker_inside.jpg" alt="drawing" width="300"/>](clicker_inside.jpg)


## Components
* 2 x AZDelivery SSD1306 OLED screen
* 1 x Raspberry Pi Zero W
* 1 x TP4056 battery charger
* 1 x MT3608 step up converter
* 1 x 5000MAh LiPo battery
* 3 x Clicker buttons
* 1 x Power button

## Pinout
![Wiring](wiring.png)
(Source: https://lucid.app/publicSegments/view/29dfcc4b-7ac9-45ab-b54a-e5f21a3d707d)

### Displays
- Left screen address: 0x3c
- Right screen address: 0x3d

### GPIO pinout
| Switch color | GPIO #|
|------|-----------|
| Red switch |25|
| Green switch (reset) |23|
| Blue switch |17|
| 5V+ input | 04 |
| 5V- input | 06 |
| Screen VCC+ | 01 |
| Screen VCC- | 09 |
| Screen SDA | 03 |
| Screen SCL | 05 |

## Casing
### Components
3D printed from `box_body.stl` using PLA for the casing. Machine cut from PMMA for the lid.

### Assembly
#### Cables
* Left screen: 4 x 5cm
* Right screen: 4 x 13 cm
* Red button: 2 x 12 cm
* Green button: 2 x 12 cm
* Blue button: 2 x 16 cm
* USB to step-up: 2 x 16 cm
* Step-up to RPI: 3 x 14 cm

