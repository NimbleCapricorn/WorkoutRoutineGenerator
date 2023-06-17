import os.path
import sys
import csv
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ExerciseClass

ExerciseList = []
Variations = []
Tempo = []
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = ExerciseClass.Exercise(row[0], row[1], row[2], row[3], row[4])
        ExerciseList.append(newExercise)
        print(newExercise)

    
