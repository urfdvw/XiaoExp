"""
Screen shake detection based on tilt ball sensor

- tiltball between [A1b] and [GND]
- 1Kohm reference resistor between [3V3] and [A1a]
"""

#%%
import board
import xiaoexp as xe
from time import sleep
#%%
sensor = xe.Rsensor(pin=board.A1, ref=1)
alarm = xe.Buzzer(pin=board.A3)
#%%
while True:
    if sensor.get_resistance() > 1:
        alarm.sound()
