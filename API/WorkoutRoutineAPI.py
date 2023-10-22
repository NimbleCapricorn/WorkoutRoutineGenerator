import os
from copy import *
from tablib import *
from pandas import *
from subprocess import *
from yaml import *
from workoutroutinegenerator import DayClass, Warmup, ProgramSettingWeekClass as WeekClass
from workoutroutinegenerator.exerciseclass import ExerciseClass
from workoutroutinegenerator.exerciseclass.difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOL_Target
from fastapi import FastAPI, Path
from typing import Optional, List
from typing import Optional, List


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
Weeks:WeekClass.ProgramSettingWeek=[]           #this list contains the week settings the program will incorporate
WorkoutDays:ExerciseClass.ProgramSettingDay=[]  #this list contains all the days the person works out on, and the exercises they do

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

@app.post("/add-single-week-setting")
def add_workout_week(VolumeSetting:Volume, IntensitySetting:Intensity, INOLSetting:INOL_Target):
    week_to_add = WeekClass.ProgramSettingWeek(VolumeSetting, IntensitySetting, INOLSetting)
    Weeks.add(week_to_add)
    return week_to_add

@app.post("/add-single-workout-day")
def add_single_workout_day(Name:str, exercise_names:List[str]):
    day_to_add=ExerciseClass.ProgramSettingDay(Name, exercise_names)
    WorkoutDays.append(day_to_add)
    return day_to_add

@app.port("/define-the-workout-week")
def define_a_workout_week(WorkoutDayNames:List[str], DailyExerciseLists:List[str]):
    WorkoutWeek:ExerciseClass.ProgramSettingDay=[]
    for dayindex, WorkoutDayName in enumerate(WorkoutDayNames):
        day_to_add=ExerciseClass.ProgramSettingDay(WorkoutDayName, DailyExerciseLists[dayindex])
        WorkoutWeek.append(day_to_add)
    WorkoutDays.clear()
    WorkoutDays.extend(WorkoutWeek)
    return WorkoutWeek
        