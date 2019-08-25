import pigpio

class Display:
    # Refresh time between pulses in µs
    REFRESH=1000

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
    }

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

        self.current_waveform_id = None
        self.current_display = [0]*len(self.digits_pinouts)

    def show(self, display_string: str):
        if len(display_string) != 4:
            raise ValueError(f"Expected length value to be 4, got{len(display_string)}")
        for i, char in enumerate(display_string):
            if char in self.CHARSET:
              self.current_display[i] = self.CHARSET[char]
            else:
              self.current_display[i] = 0
            
        self._update_display()
     
    def shutdown(self):
        self.show("    ")
        self.pi.wave_tx_stop()
        self.pi.wave_delete(self.current_waveform_id)

    def _update_display(self):
        waveform = []
        for digit_index in range(len(self.digits_pinouts)):

            segments = self.current_display[digit_index] # segments on for current digit

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
        new_waveform_id = self.pi.wave_create() # commit waveform
        self.pi.wave_send_repeat(new_waveform_id) # transmit waveform repeatedly

        if self.current_waveform_id is not None:
            self.pi.wave_delete(self.current_waveform_id) # delete no longer used waveform

        self.current_waveform_id = new_waveform_id
