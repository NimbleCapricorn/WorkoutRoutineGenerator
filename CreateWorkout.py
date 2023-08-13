import os.path
import sys
import csv
import datetime
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ExerciseClass
import ProgressionClass
import Difficulty

###########################################
#Section 1: configurations and data loading
###########################################
##
#Section 1 subsection A): configurations and definitions
##
ProgressionMethods=["Linear", "DailyUndulating", "WeeklyUndulating"]
Prilepin = ["Max", "Heavy+", "Heavy", "Mod+", "Mod", "Light+", "Light"]
PrilepinRowList=[]
ProgressionList=[]
ExerciseList=[]

#Select Exercises here
SelectedMainExercises = ["snatch", "clean", "jerk"]
SelectedPowerExercises = ["cleanPull", "snatchPull"]
SelectedTechniqueExercises =[]
SelectedStrengthExercises =["FrontSquat", "BackSquat", "MilitaryPress"]
SelectedBodybuildingExercises=[]

#Select number of weekly workouts and number of weeks here
NumberOfWeeklyWorkouts = 4
NumberOfWeeks = 12

#Select type of Block here
ProgressionSystem = "DailyUndulating"

##
#Section 1 subsection B): data loading
##
#This way of handling the prilepin chart is very artificial (as in: not intuitive). Maybe there is a better way of doing it, but I don't know how
with open("PrilepinChart.csv", "r") as PrilepinFile:
    reader = csv.reader(PrilepinFile, delimiter=";")
    
    for row in reader:
        PrilepinRowList.append(row)
        print(PrilepinRowList)
        


with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = ExerciseClass.Exercise(row[0], row[1], row[2])
        ExerciseList.append(newExercise)
        print(newExercise)

with open("Progressions.csv", "r") as ProgressionsFile:
    reader = csv.reader(ProgressionsFile, delimiter=";")
    
    for row in reader:
        newProgression = ProgressionClass.Progression(row[0], row[1], row[2])
        ProgressionList.append(newProgression)
        print(newProgression)

Block=np.array()
