import os
from copy import *
from tablib import *
from pandas import *
from subprocess import *
from yaml import *
from workoutroutinegenerator import ProgramSettingWeek, DayClass, Warmup
from workoutroutinegenerator.exerciseclass import ExerciseClass
from fastapi import FastAPI, Path
from typing import Optional


##function definitions:##
def findExercise(searching:str):
    for Exercise in ExerciseList:
        if Exercise.Name==searching:
            return Exercise
    return "Exercise not found"
##########################
##Application data and config read##
with open('Exercises.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    ExerciseList=[]
    for ExerciseConfigItem in ProgramConfig['Exercises']:
        ExerciseList.append(ExerciseClass.Exercise( ExerciseConfigItem['Name'],
                                                    ExerciseConfigItem['minRepetitions'],
                                                    ExerciseConfigItem['maxRepetitions'], 
                                                    ExerciseConfigItem['Priority'], 
                                                    ExerciseConfigItem['generateWarmup']))
#import Day settings
with open('Days.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    DaySettingList=[]
    for DayConfigItem in ProgramConfig['Weekdays']:
        DaySettingList.append(DayClass.DayClass(DayConfigItem['Name'],
                                                DayConfigItem['INOL_Priority']))

####################################
##Program Settings##
Weeks:ProgramSettingWeek=[]
Days:ExerciseClass.ProgramSettingDay=[]

#API 
app=FastAPI()

@app.get("/")
def home():
    return {"Data": "This is the homepage of the WorkoutRoutineGenerator application"}

@app.get("/about")
def about():
    return {"Data": "This application creates a WorkoutProgram with preferences you set up"}

@app.get("/get-exercise")
def get_exercise(requested_exercise: str):
    return findExercise(requested_exercise) 

@app.post("/add-exercise")
def add_exercise(name:str, minreps:int, maxreps:int, priority:float, warmup:bool):
    exercise_to_add=ExerciseClass.Exercise(name, minreps, maxreps, priority, warmup)
    ExerciseList.append(exercise_to_add)
    return exercise_to_add