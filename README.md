# py-clicker
Raspberry Pi score counter for Canne de combat

## Setup
**Version:** Rasbian Buster Lite

**Setup:**
* Configure Wifi connection / autologin in `raspi-config`
* Install the following packages:
  * adafruit-circuitpython-ssd1306 (pip)
  * python3-numpy (apt)
  * pigpio (http://abyz.me.uk/rpi/pigpio/download.html)
  * pyyaml (pip)
* Configure `clicker_config.yaml`
* Copy \*.py/\*.yaml to your home directory
* Add this line in `/etc/rc.local` before `exit 0`:
``` bash
    sudo pigpiod
```
* Add this line in /boot/config.txt
``` bash
    dtparam=i2c_arm_baudrate=1000000
```


* Add this to the end of your `.profile`:
``` bash
    # Run clicker.py only if not connected through SSH
    if [ -z "$SSH_CLIENT" ] || [ -z "$SSH_TTY" ]; then
        python3 /home/pi/py-clicker/clicker.py
    fi
```
* Reboot