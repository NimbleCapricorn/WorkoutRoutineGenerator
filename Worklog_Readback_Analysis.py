#Worklog Readback and Analysis
from xlsxwriter import *
from pandas import *
from numpy import *
with open('Output.xlsx','rb') as programfile:
    WorkoutLog=read_excel(programfile, 'WorkoutLog', header=["DateTime", "Exercise", "NumberOfSets", "NumberOfReps", "Weight", "OneRepMax", "RPE", "INOL"])