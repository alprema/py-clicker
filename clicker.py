from gpiozero import Button
from timeit import default_timer as timer
import time
import requests
import yaml
import asyncio
from digital_display import start_display_loop, stop_display_loop, display_string

RED = 'Red'
BLUE = 'Blue'

with open("clicker_config.yaml", 'r') as stream:
	try:
		configuration = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

print('Configured with identifier: ' + configuration['clicker-identifier'])

loop = asyncio.get_event_loop()
press_times = { RED: timer(), BLUE: timer() }
scores = { RED: 0, BLUE: 0 }

def button_pressed(color):
	now = timer()
	elapsed = now - press_times[color]
	press_times[color] = now
	if elapsed < 0.15: # Prevents duplicate counts since the buttons can sometimes activate twice without clicking
		return
	scores[color] += 1
	update_score()
	print('Button pressed (%s), calling URL' % color + ' ' + str(elapsed))
	loop.call_soon_threadsafe(lambda _: requests.get(configuration['outgoing-url'].format(clicker_identifier=configuration['clicker-identifier'], color=color)), '')

def reset_pressed():
    print('RESET PRESSED')
    scores[RED] = 0
    scores[BLUE] = 0
    update_score()

def update_score():
	display_string(f"{scores[RED]:02}{scores[BLUE]:02}")    

red_button = Button(4)
red_button.when_pressed = lambda _: button_pressed(RED)

blue_button = Button(18)
blue_button.when_pressed = lambda _: button_pressed(BLUE)

green_button = Button(23)
green_button.hold_time = 1 
green_button.when_held = lambda _: reset_pressed()

display_string("0000")
start_display_loop()

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Exiting")
    loop.close()

stop_display_loop()

