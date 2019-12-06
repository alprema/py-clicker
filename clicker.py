import os
import pigpio
import requests
import yaml
import asyncio
from datetime import datetime
from timeit import default_timer as timer
from display import Display

RED = 'Red'
BLUE = 'Blue'

config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "clicker_config.yaml")

with open(config_file_path, 'r') as stream:
    try:
        configuration = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print('Configured with identifier: ' + configuration['clicker-identifier'])

pi = pigpio.pi()
display = Display(pi)
loop = asyncio.get_event_loop()
scores = { RED: 0, BLUE: 0 }
log_file = open(f"clicker_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", "w+")

def button_pressed(tick, color):
    if tick - startup_tick < 100 * 1000: # Ignoring presses in the first 100 ms to avoid ghost clicks
        return
    
    scores[color] += 1
    update_score()
    print('Button pressed (%s), calling URL' % color)
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}  Blue: {scores[BLUE]} Red: {scores[RED]}\n")
    log_file.flush()
    loop.call_soon_threadsafe(lambda _: requests.get(configuration['outgoing-url'].format(clicker_identifier=configuration['clicker-identifier'], color=color)), '')


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

def update_score():
    display.show(f"{scores[RED]%100:02}{scores[BLUE]%100:02}")    


def _setup_switch(pin: int, callback, edge=pigpio.FALLING_EDGE):
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_UP)
    pi.set_glitch_filter(pin, 20 * 1000) # Time in µs
    pi.callback(pin, edge, callback)

try:
    import socket
    print(f"IP: {socket.gethostbyname('raspberrypi.local')}")
    display.show(f"ip {socket.gethostbyname('raspberrypi.local')}", show_times=2)

    display.show("0000")
    
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

