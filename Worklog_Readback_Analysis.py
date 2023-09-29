#Worklog Readback and Analysis
from xlsxwriter import *
from Difficulty import *
from pandas import *
import os

path=f"{os.getcwd()}/readback_analysis.xlsx"
with open('Output.xlsx','rb') as programfile:
    WorkoutLog=read_excel(programfile, 'WorkoutLog') #header=["DateTime", "Exercise", "NumberOfSets", "NumberOfReps", "Weight", "OneRepMax", "RPE", "INOL"]

#TODO# estimate 1RM for every row (if RPE is 0, add 0 to the reps, and calculate that way, but if RPE is filled out, use it :)) 

excel_writer=ExcelWriter(path, 'xlsxwriter')
WorkoutLog.to_excel(excel_writer)


excel_writer.close()