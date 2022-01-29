from pickletools import markobject
import csv
import numpy as np
import pandas as pd
from collections import Counter
import re
import pretty_midi
from pychord import Chord
import pygame
import music21
from sklearn.feature_extraction.text import CountVectorizer


class Chord_Generator:
    
    def __init__(self, chord='C', begin=True, corpus=[], seed=1):
        self.chord=chord
        self.begin=True
        self.corpus=corpus.to_numpy()
        self.bigrams=[]
        self.chords=[]
        self.seed = seed
        np.random.seed(self.seed)

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
        vectorizer = CountVectorizer(lowercase=False, token_pattern='\\b\\w+\\#*\\d*\\w*\\d*\\b')
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
    def convert_to_midi(self):
        midi_data = pretty_midi.PrettyMIDI()
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        piano = pretty_midi.Instrument(program=piano_program)
        length = 1
        chord_prog = [Chord(c) for c in self.chords]
        for n, chord in enumerate(chord_prog):
            for note_name in chord.components_with_pitch(root_pitch=4):
                note_number = pretty_midi.note_name_to_number(note_name)
                
                note = pretty_midi.Note(velocity=100, pitch=note_number, start=n * length, end=(n + 1) * length)
                piano.notes.append(note)
        midi_data.instruments.append(piano)
        midi_data.write('Midi_outputs/chord.mid')

        return

    def generate_chord_from_melody(self, midi):
        midi_data = pretty_midi.PrettyMIDI(midi)
        arr=[]
        
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                arr.append(pretty_midi.note_number_to_name(note.pitch))
        
        self.corpus=arr
        return arr

    def create_new_data(self):
        df = pd.DataFrame(self.corpus)
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
cg = Chord_Generator(corpus=df['chords'], chord='C')
arr = cg.generate_chord()
cg.convert_to_midi()
# print(arr)
# cg.generate_chord_from_melody('/Users/ryanshiaulam/Desktop/College/scu_grad_yr_one_RSL/Winter/COEN_219/music_duet_bot/Midi_outputs/chord.mid')
# cg.create_new_data()    
# arr = cg.generate_chord()
# print(arr)
# cg.convert_to_midi()

def play_music(midi_filename):
        '''Stream music_file in a blocking manner'''
        clock = pygame.time.Clock()
        pygame.mixer.music.load(midi_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished

freq = 44100  # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
try:
  # use the midi file you just saved
  play_music('/Users/ryanshiaulam/Desktop/College/scu_grad_yr_one_RSL/Winter/COEN_219/music_duet_bot/Midi_outputs/chord.mid')
except KeyboardInterrupt:
  # if user hits Ctrl/C then exit
  # (works only in console mode)
  pygame.mixer.music.fadeout(1000)
  pygame.mixer.music.stop()
  raise SystemExit