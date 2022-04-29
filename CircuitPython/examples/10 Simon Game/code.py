import board
import xiaoexp as xe
from ssd1306 import SSD1306_I2C
from time import sleep
from random import randrange

buzzer = xe.Buzzer()
screen = SSD1306_I2C()

class SimonButton:
    def __init__(self, loc, sym, button_pin, freq):
        self.x, self.y = loc
        self.sym = sym
        self.button = xe.Button(button_pin)
        self.freq = freq
    def press_feedback(self):
        buzzer.sound(self.freq)
        screen.print(self.sym, x=self.x, y=self.y)
    def release_feedback(self):
        buzzer.mute()
        screen.print(' ', x=self.x, y=self.y)

buttons = [
    SimonButton((60, 1), '^', board.A8, 392),
    SimonButton((0, 2), '<', board.A7, 523),
    SimonButton((120, 2), '>', board.A10, 659),
    SimonButton((60, 3), 'v', board.A9, 784),
]

dt = 0.5
sequence = [randrange(4)]
while True: # each iteration is a round
    # play the sequence
    screen.print('now playing', clrtail=True)
    for i in sequence:
        sleep(dt * 0.1)
        buttons[i].press_feedback()
        sleep(dt)
        buttons[i].release_feedback()
    
    # user input and compare the sequence
    screen.print('your turn', clrtail=True)
    seq_ind = 0
    end_turn = False
    end = False
    while True: # FSM check state loop
        for i in range(4): # each iteration detects one Simon button
            event = buttons[i].button.check()
            if event == 1:
                buttons[i].press_feedback()
            if event == -1:
                buttons[i].release_feedback()
                if i == sequence[seq_ind]: # if correct
                    seq_ind += 1
                    if seq_ind == len(sequence): # if complete
                        screen.print('good', clrtail=True)
                        sleep(1)
                        sequence.append(randrange(4))
                        print(sequence)
                        end_turn = True
                else: # if wrong
                    screen.print('your score: ' + str(len(sequence) - 1), clrtail=True)
                    end_turn = True
                    end = True
        if end_turn:
            dt *= 0.95
            break
    # reset and start a new
    if end:
        xe.gc.collect()
        print(xe.gc.mem_free())
        sleep(5)
        screen.clear()
        screen.print('touch to restart', clrtail=True)
        dt = 0.5
        sequence = [randrange(4)]
        while True:
            for i in range(4):
                event = buttons[i].button.check()
                if event == -1:
                    break
            else:
                continue
            break