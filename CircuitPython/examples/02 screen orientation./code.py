"""
Screen rotation based on tilt ball sensor

- tiltball between [A1b] and [GND]
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
while True:
    if sensor.get_resistance() > 1: # try "<" for another logic
        screen.rotate(True)
    else:
        screen.rotate(False)
    screen.print('Hello, World!', clrtail=True) # write text
    sleep(0.1)