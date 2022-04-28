"""
photoresistor average

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
filter = xe.AverageFilter(n=20, init=sensor.get_resistance())
# filter is a function with parameters (callable)
#%%
while True:
    r = sensor.get_resistance()
    screen.print('Original R (Kohm)') # use the unit of the reference resistor
    screen.print(round(r, 2), y=1, clrtail=True)
    screen.print('Average R (Kohm)', y=2) # use the unit of the reference resistor
    screen.print(round(filter(r), 2), y=3, clrtail=True) 