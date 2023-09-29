#Worklog Readback and Analysis
from xlsxwriter import *
from pandas import *
from numpy import *
import os

path=f"{os.getcwd()}/readback_analysis.xlsx"
with open('Output.xlsx','rb') as programfile:
    WorkoutLog=read_excel(programfile, 'WorkoutLog') #header=["DateTime", "Exercise", "NumberOfSets", "NumberOfReps", "Weight", "OneRepMax", "RPE", "INOL"]
    excel_writer=ExcelWriter(path, 'xlsxwriter')
    WorkoutLog.to_excel(excel_writer)
    excel_writer.close()