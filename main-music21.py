# Author: Jiakai Zhu
# CSCI 291: Computational Creativity
# Music Improvisor Project
# Date: 2022 Feb 3
# File description:
# main function that plays midi file in an infinite loop

from music21 import midi, pitch, corpus, stream
import time
import keyboard

from mido import MidiFile
# from chordgeneration import convert # Ryan's file
from pauls_melody import Paul_melody
from Bass_Generator import BassGenerator
from Chord_Generation import Chord_Generator


def main():

    # tempo
    bpm = 120
    # time signature
    beats = 4
    # phrase duration
    measures = 8
    # input file location
    music_file = '8bars.midi'
    # sleep timer
    sleep_duration = (60.0/bpm)*(measures*beats)
    # saves a copy of the music that has been played
    generatedmusic = stream.Stream()
    # keeps track of how many measures are played
    measures_played = 0
    chords = {
        "I": ('C', ['C', 'E', 'G']),
        "vi": ('Am', ['A', 'C', 'E']),
        "IV": ('F', ['F', 'A', 'C']),
        "V": ('G', ['G', 'B', 'D']),
    }

    # generate the first 8 measures
    cg = Chord_Generator(corpus=None, chord=chords, seed=1)
    generate(cg)
    mf = midi.MidiFile()
    mf.open(music_file)
    mf.read()
    mf.close()
    s = midi.translate.midiFileToStream(mf)
    sp = midi.realtime.StreamPlayer(s)

    while True:
        sp.play(blocked=False)
        start_time = time.time()
        print("current measure {}".format(measures_played))
        measures_played += measures
        cg = Chord_Generator(corpus=None, chord=chords, seed=1)
        generate(cg)
        mf = midi.MidiFile()
        mf.open(music_file)
        mf.read()
        mf.close()
        s = midi.translate.midiFileToStream(mf)
        sp = midi.realtime.StreamPlayer(s)
        time.sleep(sleep_duration + start_time - time.time())
        sp.stop()


def generate(cg):
    # call functions
    chord = Ryan_chord(cg)
    Paul_melody(chord, 32)
    Junhan_bass()

    # merge midifiles
    cv1 = MidiFile('Midi_outputs/melody.midi', clip=True)
    cv2 = MidiFile('Midi_outputs/chordAndBass.mid', clip=True)

    cv1.tracks.append(cv2.tracks[1])
    cv1.tracks.append(cv2.tracks[2])

    cv1.save('8bars.midi')


def Ryan_chord(chord_prog):
    name, matrix = chord_prog.generate_chord_progression()
    length = chord_prog.convert_to_midi(name)
    return name


def Junhan_bass():
    a = BassGenerator()
    a.generate("Midi_outputs/chord.mid",
               "Midi_outputs/chordAndBass.mid")


if __name__ == '__main__':
    main()
