import os
from copy import *
from tablib import *
from pandas import *
from subprocess import *
from yaml import *
from workoutroutinegenerator import WeekClass, DayClass, Warmup
from workoutroutinegenerator.exerciseclass import ExerciseClass
from fastapi import FastAPI, Path


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
def get_exercise(requested_exercise:str = Path(None, description="The name of the exercise you would like to see")):
    return findExercise(requested_exercise) #not found, because the ExerciseList is not populated in the API