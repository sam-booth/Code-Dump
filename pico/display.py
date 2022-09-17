from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)
display = SSD1306_I2C(128, 64, i2c)

with open('wolf.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)

display.invert(1)
display.blit(fbuf, 0, 0)
display.text("Words", 6, 55)
display.show()
