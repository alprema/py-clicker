import pigpio
from timeit import default_timer as timer
import requests
import yaml
import asyncio
from display import Display

RED = 'Red'
BLUE = 'Blue'

with open("clicker_config.yaml", 'r') as stream:
	try:
		configuration = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

print('Configured with identifier: ' + configuration['clicker-identifier'])

pi = pigpio.pi()
display = Display(pi)
loop = asyncio.get_event_loop()
scores = { RED: 0, BLUE: 0 }


def button_pressed(color):
	scores[color] += 1
	update_score()
	print('Button pressed (%s), calling URL' % color)
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
	display.show(f"{scores[RED]:02}{scores[BLUE]:02}")    

def _setup_switch(pin: int, callback, edge=pigpio.FALLING_EDGE):
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_UP)
    pi.set_glitch_filter(pin, 20 * 1000) # Time in µs
    pi.callback(pin, edge, callback)

_setup_switch(4, lambda gpio, level, tick: button_pressed(RED))
_setup_switch(18, lambda gpio, level, tick: button_pressed(BLUE))
_setup_switch(23, reset_pressed, edge=pigpio.EITHER_EDGE)


display.show("0000")


try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Exiting")
    loop.close()

display.shutdown()
pi.stop()
