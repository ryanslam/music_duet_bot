from music21 import *


class BassGenerator:

    def __init__(self):
        self.bassline = [0, -5, -2, 0, -2, -5, -7, -5]

    def getNote(self, ps, time):
        _note = note.Note(ps)
        _note.duration = duration.Duration(time)
        return _note

    def alterNotePs(self, ps):
        return ps-24

    def generateNotes(self, _chord):
        chord_duration = _chord.duration.quarterLength

        root_ps = _chord.root().ps
        third_ps = _chord.third.ps
        root_note_ps = self.alterNotePs(root_ps)
        third_note_ps = self.alterNotePs(third_ps)
        fifth_note_ps = self.alterNotePs(root_ps+6)
        low_fifth_note_ps = self.alterNotePs(root_ps-5)
        low_flat7_note_ps = self.alterNotePs(root_ps-2)
        notes = []
        for key in self.bassline:
            notes.append(self.getNote(root_note_ps+key,
                         chord_duration/len(self.bassline)))
        return notes
        # return [getNote(root_note_ps, 0.5), getNote(low_fifth_note_ps, 0.5), getNote(low_flat7_note_ps, 0.5), getNote(root_note_ps, 0.5)]

    def generate(self, midiPath):
        # read chord.mid
        musicStream = converter.parse(midiPath)

        # init bass part
        bassPart = stream.Part()
        bass = instrument.ElectricBass()
        bass.midiChannel = 2
        bassPart.insert(bass)

        for i in range(len(musicStream.elements[0])):
            # generate bass part
            ms = stream.Measure(i)
            for element in musicStream.elements[0][i]:
                if type(element) == chord.Chord:
                    notes = self.generateNotes(element)
                    for singleNote in notes:
                        ms.append(singleNote)
                if type(element) == bar.Barline:
                    ms.append(element)
            print(ms)
            bassPart.append(ms)

        # bassPart.append(bar.Barline('final'))

        musicStream.insert(0, bassPart)

        return musicStream

        # musicStream.write('midi', 'bass.mid')
        # musicStream.show()


generator = BassGenerator()

music_stream = generator.generate('chord.mid')

music_stream.show()
