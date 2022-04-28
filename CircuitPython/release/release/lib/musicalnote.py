class Frequency:
    def __init__(self):
        self.semitone = 1.05946
        self.names = {
            'C': 27.5 / self.semitone ** 9,
            'C#': 27.5 / self.semitone ** 8,
            'Db': 27.5 / self.semitone ** 8,
            'D': 27.5 / self.semitone ** 7,
            'D#': 27.5 / self.semitone ** 6,
            'Eb': 27.5 / self.semitone ** 6,
            'E': 27.5 / self.semitone ** 5,
            'F': 27.5 / self.semitone ** 4,
            'F#': 27.5 / self.semitone ** 3,
            'Gb': 27.5 / self.semitone ** 3,
            'G': 27.5 / self.semitone ** 2,
            'G#': 27.5 / self.semitone,
            'Ab': 27.5 / self.semitone,
            'A': 27.5,
            'A#': 27.5 * self.semitone,
            'Bb': 27.5 * self.semitone,
            'B': 27.5 * self.semitone ** 2,
            '': 0,
        }
    def __call__(self, note):
        name = note[:-1]
        order = int(note[-1])
        return int(self.names[name] * 2 ** order)

freq = Frequency()