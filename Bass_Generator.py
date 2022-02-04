from music21 import *
import random


class BassNoteGenerator:
    def __init__(self) -> None:
        self.state = 0
        self.matrix = [
            [0.65, 0.6, 0.7, 0.3],
            [0.15, 0.2, 0.1, 0.6],
            [0.15, 0.05, 0.2, 0],
            [0.05, 0.15, 0, 0.1],
        ]

    def get_state(self):
        rand = random.random()
        pre = self.state
        for index in range(0, len(self.matrix)):
            if self.matrix[index][pre] >= rand:
                self.state = index
                return pre
            else:
                rand = rand - self.matrix[index][pre]
        return 0

    def generate(self, root_ps):
        _state = self.get_state()
        switcher = {
            0: 0,
            1: 7,
            2: -5,
            3: -12
        }
        return switcher[_state]+root_ps


class BassGenerator:

    def __init__(self):
        self.rythms = [[1, 1, 2, 1, 1, 1, 1],
                       [1, 1, 2, 1, 2, 1], [1, 2, 1, 1, 1, 1, 1], [
                           1, 1, 1, 1, 1, 1, 1, 1], [3, 1, 3, 1], [2, 1, 2, 1], [3, 3, 1, 1], [3, 3, 2]
                       ]

    def get_rythm(self):
        first = random.choice(self.rythms)
        second = random.choice(self.rythms)
        return [first, second]

    def get_note(self, ps, time, vol):
        _note = note.Note(ps)
        _note.duration = duration.Duration(time)
        _note.volume = vol
        return _note

    def alter_note_ps(self, ps):
        return ps-24

    def generate_Notes(self, _chord, rythm):
        chord_duration = _chord.duration.quarterLength

        root_ps = _chord.root().ps
        root_note_ps = self.alter_note_ps(root_ps)
        bass_note_generator = BassNoteGenerator()

        notes = []
        for dur in rythm:
            bass_note_generator.generate(root_note_ps)
            volume_velocity = random.randrange(60, 120)
            note_ps = bass_note_generator.generate(root_note_ps)
            note_dur = chord_duration/8*dur
            notes.append(self.get_note(
                note_ps, note_dur, volume_velocity))
        return notes

    def generate(self, imputMidiPath, outputMidiPath):
        # read chord.mid
        musicStream = converter.parse(imputMidiPath)

        # init bass part
        bassPart = stream.Part()
        bass = instrument.ElectricBass()
        bass.midiChannel = 2
        bassPart.insert(bass)

        rythm = self.get_rythm()

        for i in range(len(musicStream.elements[0])):
            # generate bass part
            ms = stream.Measure(i)
            for element in musicStream.elements[0][i]:
                if type(element) == chord.Chord:
                    notes = self.generate_Notes(element, rythm[i % 2])
                    for singleNote in notes:
                        ms.append(singleNote)
                if type(element) == bar.Barline:
                    ms.append(element)
            bassPart.append(ms)

        # bassPart.append(bar.Barline('final'))

        musicStream.insert(0, bassPart)
        musicStream.write('midi', outputMidiPath)

        return musicStream


# generator = BassGenerator()

# music_stream = generator.generate('Midi_outputs/chord.mid', 'bass.mid')

# music_stream.show()
