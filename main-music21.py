# Author: Jiakai Zhu
# CSCI 291: Computational Creativity
# Music Improvisor Project
# Date: 2022 Feb 2
# File description:
# main function that plays midi file in an infinite loop

from music21 import midi, pitch, corpus, stream
import time
import keyboard

from mido import MidiFile
# from chordgeneration import convert # Ryan's file
# import bassGenerator # Juhan's file
# from pauls_melody import Paul_melody
from Chord_Generation import Chord_Generator


generatedmusic = stream.Stream()


def main():

    chords = {
        "I"     : ('C', ['C', 'E', 'G']),
        "vi"     : ('Am', ['A', 'C', 'E']),
        "IV"     : ('F', ['F', 'A', 'C']),
        "V"     : ('G', ['G', 'B', 'D']),
    }

    cg = Chord_Generator(corpus=None, chord=chords, seed=1)
    
    while True:
        try:
            # Ends the loop.
            if keyboard.is_pressed('escape'):
                break
        except:
            break

        # Ryan's Part
        name, matrix = cg.generate_chord_progression()
        length = cg.convert_to_midi(name)
        print(name, matrix, length)


    # bpm = 120
    # beats = 4
    # measures = 6
    # music_file = '8bars.midi'
    # sleep_duration = (60.0/bpm)*(measures*beats)
    # measures_played = 0

    # generate()
    # mf = midi.MidiFile()
    # mf.open(music_file)
    # mf.read()
    # mf.close()
    # s = midi.translate.midiFileToStream(mf)
    # sp = midi.realtime.StreamPlayer(s)

    # while True:
    #     sp.play(blocked=False)
    #     start_time = time.time()
    #     print("current measure {}".format(measures_played))
    #     measures_played += measures
    #     generate()
    #     mf = midi.MidiFile()
    #     mf.open(music_file)
    #     mf.read()
    #     mf.close()
    #     s = midi.translate.midiFileToStream(mf)
    #     time.sleep(sleep_duration + start_time - time.time())
    #     sp.stop()

def generate():
    # call functions
    chord = Ryan_chord()
    Paul_meoldy(chord, 32)
    Junhan_bass()

    # merge midifiles
    cv1 = MidiFile('Midi_outputs/melody.midi', clip=True)
    cv2 = MidiFile('Midi_outputs/bass.mid', clip=True)

    cv1.tracks.append(cv2.tracks[1])
    cv1.tracks.append(cv2.tracks[2])

    cv1.save('8bars.midi')

def Ryan_chord():
    print("Ryan")
    
    # return name, matrix, length


def Junhan_bass():
    print("Junhan")
    # bassGenerator.generate("Midi_outputs/chord.mid", "Midi_outputs/chordAndBass.mid")


def Paul_meoldy():
    print('Paul')

if __name__ == '__main__':
    main()
