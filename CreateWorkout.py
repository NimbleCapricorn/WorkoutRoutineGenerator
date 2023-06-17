import os
import csv
import datetime
import ExerciseClass

ExerciseList = []
Variations = []
Tempo = []
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        ExerciseList.append(row)
        print(row)

    
