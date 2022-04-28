"""
Screen brightness based on tilt ball sensor

- photoresistor between [A1b] and [GND]
- 1Kohm reference resistor between [3V3] and [A1a]
"""

#%%
import board
import xiaoexp as xe
from time import sleep
from ssd1306 import SSD1306_I2C
#%%
sensor = xe.Rsensor(pin=board.A1, ref=1)
screen = SSD1306_I2C()
#%%
screen.print('Hello, World!', clrtail=True) # write text
while True:
    brightness = int(sensor.get_resistance() * 20)
    brightness = min(brightness, 255)
    # brightness = 255 - brightness # uncomment this line to change direction
    screen.contrast(brightness)
    sleep(0.1)