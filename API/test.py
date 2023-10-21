import os
from copy import *
from tablib import *
from pandas import *
from subprocess import *
from yaml import *
from workoutroutinegenerator import WeekClass, DayClass, Warmup
from workoutroutinegenerator.exerciseclass import ExerciseClass
from fastapi import FastAPI


##function definitions:##
def findExercise(searching:ExerciseClass.Exercise):
    for Exercise in ExerciseList:
        if Exercise.Name==searching:
            return Exercise
##########################

ExerciseList:ExerciseClass.Exercise=[]
#API 
app=FastAPI()

@app.get("/")
def home():
    return {"Data": "Test"}

@app.get("/about")
def about():
    return {"Data": "This page shows general information about the webservice"}

@app.get("/get_exercise/{exercise}")
def get_exercise(requested_exercise:str):
    for exercise in ExerciseList:
        if exercise.Name==requested_exercise:
            return f'{exercise.Name}' #not found, because the ExerciseList is not populated in the API