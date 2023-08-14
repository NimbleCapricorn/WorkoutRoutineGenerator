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
#This way of handling the prilepin chart is very artificial (as in: not intuitive). 
# with open("PrilepinChart.csv", "r") as PrilepinFile:
#     reader = csv.reader(PrilepinFile, delimiter=";")    
#     for row in reader:
#         PrilepinRowList.append(row)
#         print(PrilepinRowList)


#The better way to do it is with a partial function and trendlines based on the data as two variable functions demonstrated with trendlines below
MaxIntensity=Difficulty.IntensityFunction("Max", [-0.0405, 0.6583, -5.776, 104.87])
HeavyPIntensity=Difficulty.IntensityFunction("Heavy+", [-0.0049, +0.1003, -3.411, 97.711])
HeavyIntensity=Difficulty.IntensityFunction("Heavy", [-0.01, + 0.1733, -0.4844, 92.825])
ModPIntensity=Difficulty.IntensityFunction("Mod+", [-0.0124, + 0.2095, - 0.2897, 82.753])
ModIntensity=Difficulty.IntensityFunction("Mod", [-0.0131, 0.2206, -0.1739, 77.707])
LightPIntensity=Difficulty.IntensityFunction("Light+",[-0.0124, 0.2095, -0.2897, 82.753])
LightIntensity=Difficulty.IntensityFunction("Light",[-0.0143, 0.2387, -0.0766, 72.67])


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
