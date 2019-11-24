import pigpio
import time

class Display:
    # Refresh time between pulses in µs
    REFRESH=1000
    LOOPS_PER_SCROLL=80
    
    CHARSET={
    ' ': 0b00000000,
    '0': 0b11111100,
    '1': 0b01100000,
    '2': 0b11011010,
    '3': 0b11110010,
    '4': 0b01100110,
    '5': 0b10110110,
    '6': 0b10111110,
    '7': 0b11100000,
    '8': 0b11111110,
    '9': 0b11110110,
    '-': 0b00000010,
    '.': 0b00000001,
    '=': 0b00010010,
    ',': 0b00000001,
    'a': 0b11101110,
    'b': 0b00111110,
    'c': 0b00011010,
    'd': 0b01111010,
    'e': 0b10011110,
    'f': 0b10001110,
    'g': 0b10111100,
    'h': 0b01101110,
    'i': 0b01100000,
    'j': 0b01110000,
    'k': 0b01101110,
    'l': 0b00011100,
    'm': 0b11101100,
    'n': 0b00101010,
    'o': 0b00111010,
    'p': 0b11001110,
    'q': 0b11100110,
    'r': 0b00001010,
    's': 0b10110110,
    't': 0b00001110,
    'u': 0b00111000,
    'v': 0b00111000,
    'w': 0b00111000,
    'x': 0b01101110,
    'y': 0b01100110,
    'z': 0b11011010,
    }

    SPACER=[CHARSET[' '], CHARSET['-'], CHARSET[' ']]

    # Mapping between segments and GPIO ports
    #                   a   b   c   d   e   f   g  dp
    segments_pinouts=[ 7, 21, 13, 5,  11, 12, 19, 6]

    # Mapping between digits and GPIO ports
    #                  1   2   3   4
    digits_pinouts=[ 8, 16, 20, 26]
    
    def __init__(self, pi):
        self.pi = pi
        
        for segment in self.segments_pinouts:
           self.pi.set_mode(segment, pigpio.OUTPUT)

        for digit_index in self.digits_pinouts:
           self.pi.set_mode(digit_index, pigpio.OUTPUT)

        self.current_waveform_ids = []
        self.current_display = [0]*len(self.digits_pinouts)

    def show(self, display_string: str, show_times:int = -1):
        # 18 corresponds to 18 chars + 3 spacers = 21 loops which is about the max
        # allowed by wave_chain but still allows a full IP to be displayed      
        if len(display_string) < 4 or len(display_string) > 18:
            raise ValueError(f"Expected length [4;18], got{len(display_string)}")
        
        if show_times < -1 or show_times > 255:
            raise ValueError("Expected show_times to be [-1;255]")
        
        if len(display_string) == 4 and show_times != -1:
            raise ValueError(f"You can only set show_times for scrolling display")
            
        self.current_display = [0] * len(display_string)
            
        for i, char in enumerate(display_string.lower()):
            if char in self.CHARSET:
              self.current_display[i] = self.CHARSET[char]
            else:
              self.current_display[i] = 0
            
        self._update_display(show_times)
        
        if show_times != -1:
            while self.pi.wave_tx_busy():
                time.sleep(0.1);
     
    def shutdown(self):
        self.show("    ")
        for i in range(len(self.current_waveform_ids)):
            self.pi.wave_delete(self.current_waveform_ids[i])

    def _update_display(self, show_times):
        new_waveform_ids = []
        if len(self.current_display) == 4:
            new_waveform_ids.append(self._create_waveform(self.current_display))
        else:
            string_to_show = self.current_display + self.SPACER
            for i in range(len(string_to_show)):
                current_step = string_to_show[i:] + string_to_show[:i]
                new_waveform_ids.append(self._create_waveform(current_step))
        
        
        wave_chain = []
        
        # Adding a longer loop of the first display to have it stable before the scrolling starts
        wave_chain += [255, 0] # loop start
        wave_chain += [new_waveform_ids[0]]
        initial_time = self.LOOPS_PER_SCROLL * 4
        wave_chain += [255, 1, initial_time % 255 , initial_time // 255] # loop end, repeat LOOPS_PER_SCROLL * 4 times
        
        wave_chain += [255, 0] # loop start
               
        for waveform_id in new_waveform_ids:
            wave_chain += [255, 0] # loop start
            wave_chain += [waveform_id]
            wave_chain += [255, 1, self.LOOPS_PER_SCROLL, 0] # loop end, repeat LOOPS_PER_SCROLL times
         
        if show_times == -1:
            wave_chain += [255, 3] # loop end, repeat forever
        else:
            wave_chain += [255, 1, show_times, 0] # loop end, repeat show_times
        
        self.pi.wave_chain(wave_chain)

        for i in range(len(self.current_waveform_ids)): # delete no longer used waveforms
            self.pi.wave_delete(self.current_waveform_ids[i]) 

        self.current_waveform_ids = new_waveform_ids

    def _create_waveform(self, four_digits_to_display) -> int:
        waveform = []
        for digit_index in range(len(self.digits_pinouts)):

            segments = four_digits_to_display[digit_index] # segments on for current digit

            on_mask = 0 # gpios to switch on
            off_mask = 0 # gpios to switch off

            # Set this digit on, others off
            for d in range(len(self.digits_pinouts)):
                if d == digit_index:
                    off_mask |= 1<<self.digits_pinouts[d] # Digits are enabled when their pin is grounded
                else:
                    on_mask |= 1<<self.digits_pinouts[d]

            # set used segments on, unused segments off
            for segment_index in range(8):
                if segments & 1<<(7-segment_index):
                    on_mask |= 1<<self.segments_pinouts[segment_index] # switch segment on
                else:
                    off_mask |= 1<<self.segments_pinouts[segment_index] # switch segment off

            waveform.append(pigpio.pulse(on_mask, off_mask, self.REFRESH))

        self.pi.wave_add_generic(waveform) # add pulses to waveform
        return self.pi.wave_create() # commit waveform