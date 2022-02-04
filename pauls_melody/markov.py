# Author: Jiakai Zhu
# CSCI 291: Computational Creativity
# Music Improvisor Project
# Date: 2022 Feb 2
# File description:
#   Parses the chord melody dataset:
#    > Pick an xml file and read all the notes and rests
#    > For each note, compute the interval between it and the root of the chord, assign int value 1-7 to it
#    > For rests, assign int value 0 to represent
#    > Each note is then turned into a state (interval,duration) where duration is a float, quarterNote == 1
#   Compute the transitional probability matrix for each unique note (pitch and duration)
# Citation:
#   Dataset used: https://github.com/shiehn/chord-melody-dataset


from music21 import converter, interval, note, tablature
from os.path import exists as dir_exists
import pickle


# Function Description:
#   Generates an appearence histogram for each state transition and store it as a dictionary
#   Structure: {(state1,state2):numOfAppearance}
#   Where state1 and state2 are duples (interval,duration)
# Requirements:
#   'songtitles.txt' which has the list of song titles in the chord-melody-dataset
#   chord-melody-dataset
# Output:
#   File: appear.pickle
#   Prints 'success' on console upon successful execution


def generate_appearence_list():
    with open('songtitles.txt', 'r') as file:
        Lines = file.readlines()

    duples = {}
    count = 0
    dataset_dir = "chord-melody-dataset"
    keylist = ['a', 'as', 'b', 'bs', 'c', 'cs',
               'd', 'ds', 'e', 'es', 'f', 'fs', 'g', 'gs']

    for folder in Lines:
        count += 1
        print("{0:.2%}".format(float(count)/len(Lines)))
        print("current directory: {}/{}".format(dataset_dir, folder.strip()))
        key = 0
        path = "{}/{}/{}.xml".format(dataset_dir, folder.strip(), keylist[key])
        while not dir_exists(path):
            key += 1
            path = "{}/{}/{}.xml".format(dataset_dir,
                                         folder.strip(), keylist[key])
        s = converter.parse(path)
        i = s[1].next()
        curr_chord = s[1].next('ChordWithFretBoard')
        curr_root = curr_chord.root()

        prev = (0, 4.0)
        total = 0

        while i is not None:
            if isinstance(i, note.Note) or isinstance(i, note.Rest):
                if isinstance(i, note.Note):
                    temp_itv = interval.Interval(
                        noteStart=curr_root, noteEnd=i).simpleName
                    itv = int(temp_itv[1])
                elif isinstance(i, note.Rest):
                    itv = 0
                new_dup = (prev, (itv, i.duration.quarterLength))
                if new_dup in duples.keys():
                    duples[new_dup] += 1
                else:
                    duples[new_dup] = 1
                prev = new_dup[1]
                total += 1
            elif isinstance(i, tablature.ChordWithFretBoard):
                curr_chord = i
                curr_root = curr_chord.root()
            i = i.next()

    print(duples)
    with open('appear.pickle', 'wb') as handle:
        pickle.dump(duples, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('appear.pickle', 'rb') as handle:
        a = pickle.load(handle)

    if duples == a:
        print('success')


# Function Description:
#   Generates probabiliry matrix based on the appearance histogram store it as a 2D dictionary
#   Structure: {state1:{state2:probability}}}
#   Where state1 and state2 are duples (interval,duration)
# Requirements:
#   'appear.pickle' which was computed by generate_appearence_list()
# Output:
#   File: prob.pickle
#   Prints 'success' on console upon successful execution


def generate_probability_matrix():
    with open('appear.pickle', 'rb') as handle:
        appear = pickle.load(handle)

    total = 0
    for i in appear.values():
        total += i

    print(total)

    probability = {}
    for key in appear.keys():
        if key[0] not in probability.keys():
            probability[key[0]] = {}
            probability[key[0]][key[1]] = appear[key]
        elif key[1] not in probability[key[0]].keys():
            probability[key[0]][key[1]] = appear[key]
        else:
            probability[key[0]][key[1]] += appear[key]

    numsuccess = 0
    numrow = 0

    for i in probability.keys():
        total = 0
        prob_total = 0.0
        numrow += 1
        for j in probability[i].keys():
            total += probability[i][j]

        for j in probability[i].keys():
            probability[i][j] = float(probability[i][j]) / total
            prob_total += probability[i][j]

        if (2.0-prob_total) < 1.01 and (2.0-prob_total) > 0.99:
            numsuccess += 1

    with open('prob.pickle', 'wb') as handle:
        pickle.dump(probability, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('prob.pickle', 'rb') as handle:
        a = pickle.load(handle)

    if numsuccess == numrow and probability == a:
        print("success")

    print(total)


# Function description: helper function when debugging
@staticmethod
def parsefile(songname):
    path = "{}/{}/{}.xml".format("chord-melody-dataset", songname, "a")
    s = converter.parse(path)
    i = s[1].next()
    while i is not None:
        if isinstance(i, note.Note) or isinstance(i, note.Rest):
            print(i.duration.quarterLength)
        i = i.next()


# For testing purposes
def main():
    generate_probability_matrix()


if __name__ == '__main__':
    main()
