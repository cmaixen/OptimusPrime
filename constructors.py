import csv
import sys
import random
import pprint
import xml.etree.ElementTree as ET
import numpy as np
from sets import Set
from utillities import *
from constructors import *
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
#Constructs a analytics matrix for trainingsset
def construct_analytics_matrix_trainset(filename):
    setfile= open(filename)
    print(filename)
    reader = csv.reader(setfile, delimiter=";")
    #General Statistics
    Performers_solution = []
    Insts_solution = []
    Styles_solution = []
    Years_solution = []
    Tempos_solution = []
    analytics_matrices_set = []
    set_ids = []

    for row in reader:

        #get information of trainingsset
        id_file = row[0]

        analytics_matrix = construct_analytics_matrix(id_file)

        Performers_solution.append(row[1])
        Insts_solution.append(row[3])
        Styles_solution.append(row[4])
        Years_solution.append(row[5])
        Tempos_solution.append(row[6])
        set_ids.append(id_file)
        analytics_matrices_set.append(analytics_matrix.flatten())
    return analytics_matrices_set,set_ids,Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution


#Constructs a analytics matrix for testset
def construct_analytics_matrix_testset(filename):
    set_ids = []
    analytics_matrices_set = []
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")
    for row in reader:
        #get information of trainingsset
        id = row[0]

        analytics_matrix = construct_analytics_matrix(id)

        #add elements to result
        analytics_matrices_set.append(analytics_matrix.flatten())

        set_ids.append(id)
    return analytics_matrices_set,set_ids


def construct_analytics_matrix(id):
    # columns are: C   C#  D   D#  E   F   F#  G   G#  A   A#  B
    # rows are :  0   1   2   3   4   5   6   7   8   9   10
    analytics_matrix = np.zeros((12,11))

    #Load in songxml
    tree = ET.parse("songs-xml/"+ id + ".xml")

    #get root
    root = tree.getroot()

    #TESTCODE
    test = []
    for row in list_of_note_comb(root):
        if row[1] > 1:
            test.append(row)

    test = sorted(test, key=lambda row: row[1])
    pp = pprint.PrettyPrinter()
    pp.pprint(test)
    #END TESTCODE

    #parse the file

    for measure in root.findall("part/measure"):
        for note in measure.findall("note"):
            rest = note.find("rest")
            if rest is None:

                Step = map_step_to_index(note.find("pitch/step").text)
                Octave = int(note.find("pitch/octave").text)
                #mark in matrix
                analytics_matrix[Step,Octave] += 1

    total_sum_of_notes = analytics_matrix.sum()
    analytics_matrix = np.divide(analytics_matrix, total_sum_of_notes)

    return analytics_matrix

def list_of_note_comb(root):
    set_of_notes = Set([])
    list_of_measures = []
    for measure in root.findall("part/measure"):
        substrings = all_ordered_measure_substrings(measure)
        temp_set = Set(substrings)
        set_of_notes = set_of_notes | temp_set
        list_of_measures.append(substrings)

    list_of_notes = sorted(list(set_of_notes), key=lambda row: len(row))

    list_of_measures = np.array(list_of_measures)
    note_comb_ctr = []

    for i in range(len(list_of_notes)):
        comb = list_of_notes[i]
        count = sum(sum(1 for i in row if i == comb) for row in list_of_measures)
        note_comb_ctr.append([comb, count])

    return note_comb_ctr

# Returns all posible ordered substrings in a measure
def all_ordered_measure_substrings(measure):

    # Make a list with all notes in the measure in stringform
    notes = []
    for note in measure.findall("note"):
        rest = note.find("rest")
        if rest is None :
            step = note.find("pitch/step").text
            octave = note.find("pitch/octave").text
            notes.append(step + octave)
        else:
            notes.append("R0")

    #Make all the possible combinations and return the list
    resultList=[]

    for i in range(len(notes)):
        prev = notes[i]
        resultList.append(notes[i])
        if i != notes[-1]:
            for j in range(i+1,len(notes)):
                prev += notes[j]
                resultList.append(prev)

    return resultList
