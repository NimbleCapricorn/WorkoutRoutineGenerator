import os.path
import sys
import csv
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ExerciseClass
import ProgressionClass

#Select Exercises here
SelectedMainExercises = ["snatch", "clean", "jerk"]
SelectedPowerExercises = ["cleanPull", "snatchPull"]
SelectedStrengthExercises =["FrontSquat", "BackSquat", "MilitaryPress"]

#Select number of weekly workouts here
NumberOfWeeklyWorkouts = 4

#Select type of Block here
ProgressionSystem = "Soviet"

NumberOfWeeks = 12
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
#TODO there needs to be a class that has all the main, power, strength (and whatever else gets added) that are in a daily workout, because this will just be an ordered list
i=0
WeeklySplitOfExercises = []
while i < NumberOfWeeklyWorkouts:
    if i <  len(SelectedMainExercises):
        WeeklySplitOfExercises.append(SelectedMainExercises[i])

    if i < len(SelectedPowerExercises):
        WeeklySplitOfExercises.append(SelectedPowerExercises[i])

    if i < len(SelectedStrengthExercises):
        WeeklySplitOfExercises.append(SelectedStrengthExercises[i])
i=0
Weeks = []
while i < NumberOfWeeks:
    Weeks[i] = WeeklySplitOfExercises
    print(Weeks[i])
