import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont
from typing import Optional

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
        self._clicker_name = None
        self._red_score = 0
        self._blue_score = 0

        self._width = self._left_screen.width
        self._height = self._left_screen.height

        self._score_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 60)
        self._bottom_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 7)
        self._image = Image.new("1", (self._width, self._height))
        self._draw = ImageDraw.Draw(self._image)


    def _update_screen(self, screen: SSD1306_I2C, score: int, bottom_line: str):

        from datetime import datetime

        self._draw.rectangle((0, 0, self._width, self._height), fill=0)
              
        # Draw score
        score_string = f"{score%100:02}"
        (font_width, font_height) = self._score_font.getsize(score_string)
        self._draw.text(
            (
                self._width // 2 - font_width // 2,
                (self._height // 2 - 10) - font_height // 2
            ),
            score_string,
            font=self._score_font,
            fill=255,
        )

        # Draw bottom line
        (font_width, font_height) = self._bottom_font.getsize(bottom_line)
        self._draw.text((self._width - font_width - 2, self._height - font_height), bottom_line, font=self._bottom_font, fill=125)
        
        screen.image(self._image)
        screen.show()


    def set_ip(self, ip: Optional[str]):
        self._ip = ip
        self._update_screen(self._right_screen, self._blue_score, self._ip)

    def set_clicker_name(self, clicker_name: str):
        self._clicker_name = clicker_name
        self._update_screen(self._left_screen, self._red_score, self._clicker_name)

    def set_red_score(self, score: int):
        self._red_score = score
        self._update_screen(self._left_screen, self._red_score, self._clicker_name)


    def set_blue_score(self, score: int):
        self._blue_score = score
        self._update_screen(self._right_screen, self._blue_score, self._ip)

     
    def shutdown(self):
        self._left_screen.fill(0)
        self._left_screen.show()

        self._right_screen.fill(0)
        self._right_screen.show()
