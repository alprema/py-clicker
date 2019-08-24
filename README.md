# py-clicker
Raspberry Pi score counter for Canne de combat

## Setup
**Version:** Rasbian Buster Lite

**Setup:**
* Configure Wifi connection / autologin in `raspi-config`
* Install pigpio (http://abyz.me.uk/rpi/pigpio/download.html)
* Configure `clicker_config.yaml`
* Copy \*.py/\*.yaml to your home directory
* Add this line in `/etc/rc.local` before `exit 0`:
``` bash
    sudo pigpio
```
* Add this to the end of your `.profile`:
``` bash
    # Run clicker.py only if not connected through SSH
    if [ -z "$SSH_CLIENT" ] || [ -z "$SSH_TTY" ]; then
        python3 /home/pi/clicker.py
    fi
```
* Reboot