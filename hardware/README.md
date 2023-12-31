# Version 2 - improvement proposal
## Hardware
### Same components
* 1 x Raspberry Pi Zero W 
* 3 x Clicker buttons
* 1 x Power button
* 1 x 3000MAh LiPo battery (TBC, see power section below)

### New components
#### Display

[This kind of display](https://www.waveshare.com/product/raspberry-pi/displays/2.42inch-oled-module.htm) would allow a broader range of info to be available, while retaining a small form factor and lower power consumption. Its ability to be plugged directly on top of the RPi Zero would also improve the wiring (and assembly) a lot.

Waveshare offers quite a range of displays and has solid expertise and documentation, in addition to being fairly competitive in terms of pricing.

### Power supply

As we've established, the Powerboost might be a bit overkill for this specific project.

Option 1 would be to go with a simpler Lipo Charging circuit, as we've discussed together. I'm not sure, however, that a LiPo pack without a booster would be beefy enough to power a RPi Zero -- does Vladimir have any input on this ?

Option 2 would be, IMHO, to power the whole thing with a portable battery pack  (those that are readily available for people with iPhones), as it's explicitely meant for powering 5V devices. 


# Version 1 - working as of december 2023
## Hardware
### Components
* 7 x 200Ω resistors
* 1 x 4 digits 7 segment common cathode display (ATA8041AW)
* 1 x Raspberry Pi Zero W
* 1 x PowerBoost 1000 Charger
* 1 x 3000MAh LiPo battery
* 3 x Clicker buttons
* 1 x Power button
* 1 x ~65mm x ~75mm prototype board

### Pinout
![Wiring](wiring.png)
(Source: https://www.lucidchart.com/invitations/accept/e652c709-daa6-480c-b3a0-5e042be13df4)

#### Display
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
#### Switches
| Switch color | GPIO #|
|------|-----------|
|Red|25|
|Green|23|
|Blue|17|

### Casing
#### Components
Velleman case G738 (https://www.velleman.eu/products/view?id=60941)

#### Cutout diagram
![CutoutSchema](casing_cutout.jpg)
The screen board needs to be 7.5cm x 6.5cm (8 3-holes connectors)

#### Assembly
##### Cables
* Raspberry to screen board: 7cm
* Raspberry to buttons: 10cm
* Raspberry to power supply: 17cm
* Power supply to switch: 17cm

##### Spacers
Nylon auto-adhesive spacers 
* Power supply: HC-5
* Raspberry: HC-8
* Screen board: HC-6
