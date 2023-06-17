import os
import csv
import datetime
import ExerciseClass

ExerciseList = []
Variations = []
Tempo = []
with open("Exercise.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile)
    
    for row in reader:
        ExerciseList.append(row)
        print(row)

    
