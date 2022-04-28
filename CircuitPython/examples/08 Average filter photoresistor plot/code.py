"""
photoresistor average

- photoresistor between [A1b] and [GND]
- 1Kohm reference resistor between [3V3] and [A1a]

Run the code in CircuitPython Online IDE,
check the sensor reading by "Plot".
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
print('startplot:', 'Original_R_(Kohm)', 'Average_R_(Kohm)')
while True:
    r = sensor.get_resistance()
    print(round(r, 4), round(filter(r), 4))
    sleep(0.1)