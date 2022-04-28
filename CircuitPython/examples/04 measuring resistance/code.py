"""
Resistance measurement

Experiment 1, measuring the resistance of solution/soil
- soil moisture probe between [A1b] and [GND]
- 1Kohm reference resistor between [3V3] and [A1a]

Experiment 2, measuring the resistance of skin
- 10Mohm reference resistor between [3V3] and [A1a]
- Fingure on the SBU logo
"""

#%%
import board
import xiaoexp as xe
from time import sleep
from ssd1306 import SSD1306_I2C
#%%
sensor = xe.Rsensor(pin=board.A1, ref=1) # change the value according to real setting
screen = SSD1306_I2C()
#%%
while True:
    screen.print('Resistance (Kohm)') # use the unit of the reference resistor
    screen.print(sensor.get_resistance(), y=1, clrtail=True)
    sleep(0.1)