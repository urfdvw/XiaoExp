"""
This CircuitPython model is written for is for the traffic light development board.

CircuitPython version: 7
microcontroller: Seeedurino Xiao SAMD21

Pins:
    A0, A1, A6 ~ A10: alligator clip, touch
    A3: buzzer
    SCL, SDA: SSD1306 OLED screen
"""
import gc
gc.enable()
import board

from time import monotonic
from time import sleep
class Timer:
    def __init__(self, hold=False):
        self.duration = 0
        self.start_time = monotonic()
        self.enable = False
        self.hold = hold
    def over(self):
        out = (monotonic() > (self.start_time + self.duration)) and self.enable
        if out and not self.hold:
            self.enable = False
        return out
    def start(self, duration):
        self.duration = duration
        self.start_time = monotonic()
        self.enable = True
    def disable(self):
        self.enable = False
        
import touchio
class Button:
    def __init__(self, pin):
        self.touch = touchio.TouchIn(pin)
        self.need_init = True
        self.current = False
        self.last = False

    def check(self):
        # init on the first check
        if self.need_init:
            sleep(0.1)
            self.touch.threshold = self.touch.raw_value + 100
            self.need_init = False
        # compute output
        self.current = self.touch.value
        out = None
        if self.current and (not self.last):
            out = 1 # press edge
        elif (not self.current) and self.last:
            out = -1 # release edge
        elif self.current and self.last:
            out = 2 # hold
        else: # idle
            out = 0
        self.last = self.current
        return out
    
import pwmio
class Buzzer:
    def __init__(self, pin=board.A3, freq=880):
        self.buzzer = pwmio.PWMOut(pin, variable_frequency=True)
        self.buzzer.duty_cycle = 0
        self.on = False
        self.freq = freq
    def show(self):
        self.buzzer.frequency = self.freq
        self.buzzer.duty_cycle = 32768 if self.on else 0
    def set_freq(self, freq):
        if freq == 0:
            self.on = False
        else:
            self.freq = freq
        self.show()
    def sound(self, freq=None):
        self.on = True
        if freq is not None:
            self.set_freq(freq)
        self.show()
    def mute(self):
        self.on = False
        self.show()
    def beep(self, freq=None, duration=0.01):
        self.sound(freq)
        sleep(duration)
        self.mute()

import analogio
# resistance sensor class
class Rsensor:
    def __init__(self, pin=board.A1, ref=1, vcc=3.3):
        self.adc = analogio.AnalogIn(pin)
        self.vcc = vcc
        self.ref = ref
        bit = 16 # ADCs on SAMD21 are 16 bit
        self.maxraw = 2 ** bit - 1
    def get_adc(self):
        return self.adc.value
    def get_norm(self):
        return self.get_adc() / self.maxraw
    def get_voltage(self):
        return self.get_norm() * self.vcc
    def get_resistance(self):
        raw = self.get_adc()
        return raw / (self.maxraw - raw) * self.ref

class AverageFilter:
    def __init__(self, n, init=0):
        self.n = n
        self.data = [init] * n
        self.i = 0
        self.sum = init * n
    def __call__(self, x):
        self.sum = self.sum - self.data[self.i] + x
        self.data[self.i] = x
        self.i += 1
        self.i %= self.n
        return self.sum / self.n
    def mean(self, x):
        return self(x)

gc.collect()