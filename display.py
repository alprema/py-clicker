import board
import os
import busio
from adafruit_ssd1306 import SSD1306_I2C
from typing import Optional
from enum import Enum

from adafruit_framebuf import BitmapFont


class Side(Enum):
    Left = 0
    Right = 1

class Display:
   
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self._left_screen: SSD1306_I2C = SSD1306_I2C(128, 64, i2c, addr=0x3c)
        self._left_screen.fill(0)
        self._left_screen.show()

        self._right_screen: SSD1306_I2C = SSD1306_I2C(128, 64, i2c, addr=0x3d)
        self._right_screen.fill(0)
        self._right_screen.show()

        self._ip = None
        self._previous_ip = None
        self._clicker_name = None
        self._previous_clicker_name = None
        self._red_score = 0
        self._previous_red_score = 0
        self._blue_score = 0
        self._previous_blue_score = 0

        self._width = self._left_screen.width
        self._height = self._left_screen.height

        self._font_location = os.path.join(os.path.dirname(__file__), "font5x8.bin")
        font = BitmapFont(self._font_location)
        self._font_base_width = font.font_width
        self._font_base_height = font.font_height



    def _print_score(self, screen: SSD1306_I2C, score: int, color: int):
        score_string_size = 5
        digits = 1 if score < 10 else 2

        string_width = digits * self._font_base_width * score_string_size + ((digits - 1) * score_string_size)
        string_height = self._font_base_height * score_string_size

        screen.text(
            str(score),
            self._width // 2 - string_width // 2,
            self._height // 2 - string_height // 2,
            color,
            font_name=self._font_location,
            size=score_string_size
        )
    
    def _print_bottom_line(self, screen: SSD1306_I2C, text: Optional[str], color: int):
        if text is None:
            return

        bottom_string_size = 1
        digits = len(text)

        string_width = digits * self._font_base_width * bottom_string_size + ((digits - 1) * bottom_string_size)
        string_height = self._font_base_height * bottom_string_size

        screen.text(
            text,
            self._width - string_width,
            self._height - string_height,
            color,
            font_name=self._font_location,
            size=bottom_string_size
        )


    def _update_score(self, side: Side):
        if side == Side.Left:
            previous_score = self._previous_red_score
            score = self._red_score
            screen = self._left_screen
            self._previous_red_score = self._red_score
        else:
            previous_score = self._previous_blue_score
            score = self._blue_score
            screen = self._right_screen
            self._previous_blue_score = self._blue_score
        

        # Display the previous score in black before the current score in white,
        # thus clearing it by sending as few pixels as possible to the screen (faster)
        self._print_score(screen, previous_score, color=0)
        self._print_score(screen, score, color=1)
        
        screen.show()


    def _update_bottom_line(self, side: Side):
        if side == Side.Left:
            previous_bottom_line = self._previous_clicker_name
            bottom_line = self._clicker_name
            screen = self._left_screen
            self._previous_clicker_name = self._clicker_name
        else:
            previous_bottom_line = self._previous_ip
            bottom_line = self._ip
            screen = self._right_screen
            self._previous_ip = self._ip

           
        self._print_bottom_line(screen, previous_bottom_line, color=0)
        self._print_bottom_line(screen, bottom_line, color=1)      


    def set_ip(self, ip: Optional[str]):
        self._ip = ip
        self._update_bottom_line(Side.Right)

    def set_clicker_name(self, clicker_name: str):
        self._clicker_name = clicker_name
        self._update_bottom_line(Side.Left)

    def set_red_score(self, score: int):
        self._red_score = score
        self._update_score(Side.Left)


    def set_blue_score(self, score: int):
        self._blue_score = score
        self._update_score(Side.Right)

     
    def shutdown(self):
        self._left_screen.fill(0)
        self._left_screen.show()

        self._right_screen.fill(0)
        self._right_screen.show()
