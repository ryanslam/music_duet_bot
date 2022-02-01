import csv
from typing import KeysView
import numpy as np
import pandas as pd
from collections import Counter
import re
import pretty_midi
from pychord import Chord
import pygame
from sklearn.feature_extraction.text import CountVectorizer

    
class Chord_Generator:
    
    def __init__(self, chord=[], begin=True, corpus=[], seed=None):
        self.chord=chord
        self.begin=True
        self.corpus=corpus
        self.bigrams=[]
        self.chords=chord
        self.seed = seed
        np.random.seed(self.seed)
    
    def obtain_possible_chords(self):
        chords = []
        for val in self.chords.keys():
            chords.append(val)
        return chords
    
    def calc_prob(self, chord=None):
        options = self.obtain_possible_chords()
        if not(chord):
            chord = np.random.choice(options)
            prob = 0
        elif (chord=='IV'):
            chord = ['IV', 'I', 'V']
            prob = [.15, .15, .7]
        elif (chord=='V'):
            chord = ['IV', 'V', 'vi']
            prob = [.15, .15, .7]
        elif (chord=='vi'):
            chord = ['V', 'vi', 'I']
            prob = [.15, .15, .7]
        else:
            chord = ['vi', 'I', 'IV']
            prob = [.15, .15, .7]
        return (chord, prob)

    def generate_chord_progression(self, bars=8):
        temp_name = []
        temp_chord = []
        chord_name_arr = []
        chord_matrix = []
        options, prob = self.calc_prob()
        for i in range(4*bars):
            if i == 0:
                chord = options
            else:
                # print(options, prob)
                chord = np.random.choice(options, p=prob)
            temp_chord.append(chord)
            
            options, prob = self.calc_prob(chord)

        for i in range(len(temp_chord)):
            name, chord = self.chords.get(temp_chord[i])
            temp_name.append(name)
            temp_chord[i] = chord

        
        for i in range(len(temp_chord)):
            # print(len(temp_name))
            # if i%2 == 0 and not(i == 0):
            #     chord_name_arr.append('Fm')
            #     chord_matrix.append('.')
            # print(i)
            chord_name_arr.append(temp_name[i])
            chord_matrix.append(temp_chord[i])
        #     print(chord_matrix)
        # print(chord_name_arr)
        # print(chord_matrix)
        return (chord_name_arr, chord_matrix)

    # Generates the bigrams of the chords given a chord csv.
    def generate_bigrams(self):
        ngrams = zip(*[self.corpus[i:] for i in range(2)])
        bigrams = [" ".join(ngram) for ngram in ngrams]
        bigrams = [bigram for bigram in bigrams if bigram.split(' ')[0]==self.chord]
        return bigrams

    # Predicts the next chord given the previous chord.
    def markov_prediction(self):
        # Convert bigrams according to chord.
        bigrams = self.generate_bigrams()
        for chord in range(len(bigrams)):
            bigrams[chord] = re.sub(".+? ", "", bigrams[chord])
        # print(bigrams)
        vectorizer = CountVectorizer(lowercase=False, token_pattern='\\b\\w+\\-*\\#*\\d*\\w*\\d*\\b')
        freq = vectorizer.fit_transform(bigrams).sum(axis=0)
        freq = np.squeeze(np.asarray(freq))
        options = vectorizer.get_feature_names_out()
        probability_matrix = freq/len(bigrams)
        if len(options) == 1:
            return options[0]
        return np.random.choice(options, p=probability_matrix)

    # Generates a combination of chords.    
    def generate_chord(self):
        # Generate 8-bar; quarter notes = 28 notes.
        self.chords = []
        for notes in range(12):
            self.chords.append(self.markov_prediction())
            self.chord = self.chords[-1]
        return self.chords

    # Converts the generated chords to a midifile.
    def convert_to_midi(self, chord_prog):
        midi_data = pretty_midi.PrettyMIDI()
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        piano = pretty_midi.Instrument(program=piano_program)
        length = 4
        vol = 100
        
        chord_prog = [Chord(c) for c in chord_prog]
        print(len(chord_prog))
        for n, chord in enumerate(chord_prog):
            if str(chord) == 'Fm':
                vol = 0
            else:
                vol = 100
            # print(chord)
            for note_name in chord.components_with_pitch(root_pitch=4):
                note_number = pretty_midi.note_name_to_number(note_name)
                note = pretty_midi.Note(velocity=vol, pitch=note_number, start=n*length, end=(n + 1) * length)
                
                piano.notes.append(note)
        midi_data.instruments.append(piano)
        midi_data.write('Midi_outputs/chord.mid')

        return

    # Takes in an input MIDI and extracts the note names.
    def generate_chord_from_melody(self, midi):
        midi_data = pretty_midi.PrettyMIDI(midi)
        arr=[]
        
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                arr.append(pretty_midi.note_number_to_name(note.pitch))
        
        self.corpus=arr
        return arr

    # Uses the melody as a new dataset for the next chord progression.
    def create_new_data(self):
        df = pd.DataFrame(self.chords)
        df.columns = ['chords']
        self.corpus = df['chords'].to_numpy()
        print(self.corpus)
        # Generate next chord progression from most common chord in melody.
        unique,pos = np.unique(self.corpus,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()  
        self.chord = unique[maxpos]
        print(self.chord)
        return

df = pd.read_csv('chord_generation_data/chords.csv')



chords = {
        "I"     : ('C', ['C', 'E', 'G']),
        "vi"     : ('Am', ['A', 'C', 'E']),
        "IV"     : ('F', ['F', 'A', 'C']),
        "V"     : ('G', ['G', 'B', 'D']),
    }
cg = Chord_Generator(corpus=None, chord=chords, seed=1)
name, matrix = cg.generate_chord_progression()
print(name)
print(matrix)
cg.convert_to_midi(name)
# cg.generate_chord_from_melody('/Users/ryanshiaulam/Desktop/College/scu_grad_yr_one_RSL/Winter/COEN_219/music_duet_bot/Midi_outputs/chord.mid')
# cg.create_new_data()    
# arr = cg.generate_chord()
# print(arr)
# cg.convert_to_midi()

# def play_music(midi_filename):
#         '''Stream music_file in a blocking manner'''
#         clock = pygame.time.Clock()
#         pygame.mixer.music.load(midi_filename)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             clock.tick(30) # check if playback has finished

# freq = 44100  # audio CD quality
# bitsize = -16   # unsigned 16 bit
# channels = 2  # 1 is mono, 2 is stereo
# buffer = 1024   # number of samples
# pygame.mixer.init(freq, bitsize, channels, buffer)
# try:
#   # use the midi file you just saved
#   play_music('/Users/ryanshiaulam/Desktop/College/scu_grad_yr_one_RSL/Winter/COEN_219/music_duet_bot/Midi_outputs/chord.mid')
# except KeyboardInterrupt:
#   # if user hits Ctrl/C then exit
#   # (works only in console mode)
#   pygame.mixer.music.fadeout(1000)
#   pygame.mixer.music.stop()
#   raise SystemExit