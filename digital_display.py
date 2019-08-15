from gpiozero import OutputDevice
from threading import Thread
import time
 
# GPIO ports for the 7seg pins + decimal separator
segments_pinout =  (25,12,6,22,5,24,13,19)
segments = []
 
for segment_pin in segments_pinout:
    segments.append(OutputDevice(segment_pin))
 
# GPIO ports for the digit pins 
digits_pinout = (16,20,21,17)
digits = []
 
for digit_pin in digits_pinout:
    digits.append(OutputDevice(digit_pin, initial_value=True))
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
 
_display_string = "1234"

_thread: Thread = None
_is_running = True

def _inner_loop():
    while _is_running:
        for digit in range(4):
            for loop in range(0,7):
                current_digit = _display_string[digit]
                segments[loop].on() if num[current_digit][loop] else segments[loop].off()
            
            segments[7].off()
            
            #if int(time.time()) % 4 == digit:
            #    segments[7].on()
                
            digits[digit].off()
            time.sleep(0.001)
            digits[digit].on()


def display_string(display_string: str):
    global _display_string
    _display_string = display_string
    
def start_display_loop():
    global _thread
    _thread = Thread(target=_inner_loop)
    _thread.start()
    
def stop_display_loop():
    global _is_running
    _is_running = False
    _thread.join()
