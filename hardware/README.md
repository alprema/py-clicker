# Hardware
## Components
* 7 x 200Ω resistors
* 1 x 4 digits 7 segment common cathode display (ATA8041AW)
* 1 x Raspberry Pi Zero W
* 1 x PowerBoost 1000 Charger
* 1 x 3000MAh LiPo battery
* 3 x Clicker buttons
* 1 x Power button
* 1 x ~65mm x ~75mm prototype board

## Pinout
![Wiring](wiring.png)
(Source: https://www.lucidchart.com/invitations/accept/e652c709-daa6-480c-b3a0-5e042be13df4)

### Display
| 7-segment pin | GPIO #| Resistor |
|------|-----------|-------|
|1|11|Y
|2|5|Y
|3|6|Y
|4|13|Y
|5|19|Y
|6|26|N
|7|21|Y
|8|20|N
|9|16|N
|10|12|Y
|11|7|Y
|12|8|N
### Switches
| Switch color | GPIO #|
|------|-----------|
|Red|25|
|Green|23|
|Blue|17|

## Casing
### Components
Velleman case G738 (https://www.velleman.eu/products/view?id=60941)

### Cutout diagram
![CutoutSchema](casing_cutout.jpg)