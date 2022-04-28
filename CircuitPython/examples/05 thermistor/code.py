"""
Thermistor

- thermistor between [A1b] and [GND]
- 10Kohm reference resistor between [3V3] and [A1a]
"""

import board
import xiaoexp as xe
from time import sleep
from ssd1306 import SSD1306_I2C
from math import log

# Reference resistor
r_ref = 10

# calculate temperature according to resistance
def r2temp(r):
    B = 3820 # Sensor Parameter
    return 1 / ((log(r) - log(10))/B + 1/(25+273.15)) - 273.15

sensor = xe.Rsensor(pin=board.A1, ref=10) # change the value according to real setting
screen = SSD1306_I2C()

while True:
    r_sensor = sensor.get_resistance()
    temp = r2temp(r_sensor)
    screen.print(str(r_sensor) + ' Kohm', clrtail=True)
    screen.print(str(temp) + ' C', clrtail=True, y=1)
    sleep(0.5)
