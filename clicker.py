import os
import pigpio
import requests
import yaml
import json
import asyncio
from datetime import datetime
from timeit import default_timer as timer
from enum import Enum
from display import Display

RED = 'Red'
BLUE = 'Blue'

class PressType(Enum):
    long_press="long_press"
    short_press="short_press"

config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "clicker_config.yaml")

with open(config_file_path, 'r') as stream:
    try:
        configuration = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

print('Configured with identifier: ' + configuration['clicker-identifier'])

first_click_made = False
pi = pigpio.pi()
display = Display()
loop = asyncio.get_event_loop()
scores = { RED: 0, BLUE: 0 }
api_call_count = 0
log_file = open(f"clicker_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", "w+")

def call_api(button: int, press_type: PressType):
    global api_call_count
    api_call_count += 1
    data = {
        "serial": configuration['clicker-identifier'],
        "buttonId": button,
        "typeClick": press_type.value,
        "internalState": {
            "0": api_call_count,
            "1": scores[RED],
            "2": scores[BLUE]
        }
    }
    
    requests.post(configuration['outgoing-url'], data=json.dumps(data), headers={"Content-Type": "application/json", "X-Requested-With":"XMLHttpRequest"})

def button_pressed(tick, color):
    global first_click_made
    # Ignoring presses in the first 100 ms to avoid ghost clicks
    # but using first_click_made to prevent ignoring clicks after wraparound every 71.6 minutes
    if not first_click_made and tick - startup_tick < 100 * 1000: 
        return
    
    first_click_made = True
    
    scores[color] += 1
    
    if color == RED:
        display.set_red_score(scores[RED])
    else:
        display.set_blue_score(scores[BLUE])

    print('Button pressed (%s), calling URL' % color)
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}  Blue: {scores[BLUE]} Red: {scores[RED]}\n")
    log_file.flush()
    loop.call_soon_threadsafe(lambda _: call_api(1 if color == RED else 2, PressType.short_press), '')


_last_reset_press_tick = pi.get_current_tick()

def reset_pressed(gpio, level, tick):
    global _last_reset_press_tick
    if level == 0:
        _last_reset_press_tick = tick
        pi.set_watchdog(gpio, 1000)
        return
    
    pi.set_watchdog(gpio, 0)
    
    if level == 2:
        pressed_time_micros = pigpio.tickDiff(_last_reset_press_tick, tick)
        if pressed_time_micros < 1000 * 1000:
            return
        print('RESET PRESSED')
        scores[RED] = 0
        scores[BLUE] = 0
        update_score()
        loop.call_soon_threadsafe(lambda _: call_api(0, PressType.long_press), '')

def update_score():
    display.set_red_score(scores[RED])
    display.set_blue_score(scores[BLUE])

def _setup_switch(pin: int, callback, edge=pigpio.FALLING_EDGE):
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_UP)
    pi.set_glitch_filter(pin, 20 * 1000) # Time in µs
    pi.callback(pin, edge, callback)

try:
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(f'{hostname}.local')
    print(f"IP: {ip}")

    display.set_ip(ip)
    display.set_clicker_name(configuration['clicker-identifier'].split("_")[0])
    display.set_red_score(0)
    display.set_blue_score(0)
    
       
    startup_tick = pi.get_current_tick()
    _setup_switch(25, lambda gpio, level, tick: button_pressed(tick, RED))
    _setup_switch(17, lambda gpio, level, tick: button_pressed(tick, BLUE))
    _setup_switch(23, reset_pressed, edge=pigpio.EITHER_EDGE)

    loop.run_forever()
except KeyboardInterrupt:
    print("Exiting")
    log_file.close()
    loop.close()

display.shutdown()
pi.stop()

