import os.path
import sys
import csv
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ExerciseClass
import ProgressionClass

ExerciseList = []
Variations = []
Tempo = []
PrilepinRowList = []
PrilepinTable = []
Prilepin = ["Reps", "Max", "Heavy+", "Heavy", "Mod+", "Mod", "Light+", "Light"]
ProgressionList = []

#This way of handling the prilepin chart is very artificial (as in: not intuitive). Maybe there is a better way of doing it, but I don't know how
with open("PrilepinChart.csv", "r") as PrilepinFile:
    reader = csv.reader(PrilepinFile, delimiter=";")
    
    for row in reader:
        PrilepinRowList.append(row)
        print(PrilepinRowList)


with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = ExerciseClass.Exercise(row[0], row[1], row[2], row[3], row[4])
        ExerciseList.append(newExercise)
        print(newExercise)

with open("Progressions.csv", "r") as ProgressionsFile:
    reader = csv.reader(ProgressionsFile, delimiter=";")
    
    for row in reader:
        newProgression = ProgressionClass.Progression(row[0], row[1], row[2])
        ProgressionList.append(newProgression)
        print(newProgression)

