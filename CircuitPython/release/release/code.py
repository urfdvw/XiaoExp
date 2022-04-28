"""
Test code for the hardware

Result:
- buzzer makes Mario sound
- touch A0 (SBU logo) will change the voltage reading on the OLED screen
- touch A1, A6 ~ A10 will show the pin names on the OLED screen
"""

#%%
import board
import xiaoexp as xe
from time import sleep
from ssd1306 import SSD1306_I2C

#%% Test RGB LED and buzzer

## mario song
notes = "3330135"
durations = "8488844"

note2freq = { 
    '1': 523,
    '3': 659,
    '5': 784,
}

## play the song
buzzer = xe.Buzzer()
for i in range(len(notes)):
    duration = 1 / int(durations[i])
    if notes[i] != '0':
        buzzer.sound(note2freq[notes[i]])
    sleep(duration * 0.5)
    buzzer.mute()
    sleep(duration * 0.5)
    
#%% Test input and OLED screen
screen = SSD1306_I2C()
sensor = xe.Rsensor()
buttons = [
    xe.Button(board.A0),
    xe.Button(board.A6),
    xe.Button(board.A7),
    xe.Button(board.A8),
    xe.Button(board.A9),
    xe.Button(board.A10),
]
names = ['A0', 'A6', 'A7', 'A8', 'A9', 'A10']
y = [0, 0, 1, 1, 2, 2]
x = [0, 60, 0, 60, 0, 60]

#%% loop
timers = [xe.Timer() for i in range(6)] # Timer for the touch
while True:
    for i in range(6): #
        if buttons[i].check() == 1:
            screen.print(names[i], x[i], y[i])
            print(names[i], '-' * 30)
            print(buttons[i].touch.threshold)
            print(buttons[i].touch.raw_value)
            timers[i].start(1.0)
        if timers[i].over():
            screen.print('   ', x[i], y[i])
    screen.print('A0 vol: ' + str(round(sensor.get_voltage(), 3)), y=3, clrtail=True)