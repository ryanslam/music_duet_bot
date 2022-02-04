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
# import bassGenerator # Juhan's file
from pauls_melody import Paul_melody


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

    # generate the first 8 measures
    generate()
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
        generate()
        mf = midi.MidiFile()
        mf.open(music_file)
        mf.read()
        mf.close()
        s = midi.translate.midiFileToStream(mf)
        sp = midi.realtime.StreamPlayer(s)
        time.sleep(sleep_duration + start_time - time.time())
        sp.stop()


def generate():
    # call functions
    chord = Ryan_chord()
    Paul_melody(chord, 32)
    Junhan_bass()

    # merge midifiles
    cv1 = MidiFile('Midi_outputs/melody.midi', clip=True)
    cv2 = MidiFile('Midi_outputs/bass.mid', clip=True)

    cv1.tracks.append(cv2.tracks[1])
    cv1.tracks.append(cv2.tracks[2])

    cv1.save('8bars.midi')


def Ryan_chord():
    print("Ryan")
    # chords = {
    #     "I"     : ('C', ['C', 'E', 'G']),
    #     "vi"     : ('Am', ['A', 'C', 'E']),
    #     "IV"     : ('F', ['F', 'A', 'C']),
    #     "V"     : ('G', ['G', 'B', 'D']),
    # }
    # cg = Chord_Generator(corpus=None, chord=chords)
    # name, matrix = cg.generate_chord_progression()
    # print(name)
    # cg.convert_to_midi(name)
    # return name

    return ['F', 'A', 'G', 'C', 'B', 'E', 'A', 'D', 'G', 'A', 'F', 'G', 'D', 'G', 'C', 'C', 'F', 'A', 'G', 'C', 'B', 'E', 'A', 'D', 'G', 'A', 'F', 'G', 'D', 'G', 'C', 'C']


def Junhan_bass():
    print("Junhan")
    # bassGenerator.generate("Midi_outputs/chord.mid", "Midi_outputs/chordAndBass.mid")


if __name__ == '__main__':
    main()
