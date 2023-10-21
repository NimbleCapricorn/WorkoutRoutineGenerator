#!/usr/bin/env python3 
#this script requires python 3.10+, as match cases are only supported by those versions.
import os
from copy import *
from tablib import *
from pandas import *
from subprocess import *
from yaml import *
from workoutroutinegenerator import WeekClass, DayClass, Warmup
from workoutroutinegenerator.exerciseclass import ExerciseClass

##function definitions:##
def findExercise(searching:ExerciseClass.Exercise):
    for Exercise in ExerciseList:
        if Exercise.Name==searching:
            return Exercise
##########################

##config parsing##
#import exercise settings   
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

#program block setting parsing
with open('ProgramConfig.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    ProgramSettingDays=[]
    for DayConfigItem in ProgramConfig['Workoutdays']:
        ProgramSettingDays.append(ExerciseClass.ProgramSettingDay(DayConfigItem['Name'],
                                                                  DayConfigItem['ExerciseList']))
    Weeks=[]
    for WeekConfigItem in ProgramConfig['Weeks']:
        VolumeSetting=WeekClass.searchVolumeSetting(WeekConfigItem['Volume'])
        IntensitySetting=WeekClass.searchIntensitySetting(WeekConfigItem['Intensity'])
        INOL_TargetSetting=WeekClass.searchINOLSetting(WeekConfigItem['INOL_Target'])
        Weeks.append(WeekClass.WeekSetting(VolumeSetting, IntensitySetting, INOL_TargetSetting))
##################################################
#Frontend development flags:
generateWorkoutLog:bool=False
generateExcelOutput:bool=True
##################################################
## program data creation
ListOfExercises:ExerciseClass.DailyExercise=[]
DayINOLSetting:float
for weekindex, week in enumerate(Weeks):
    for Day in ProgramSettingDays:
        for exercise in Day.ExerciseList:
            #generate the working sets:
            for DayIterator in DaySettingList: 
                if DayIterator.name == Day.Name: 
                    DayINOLSetting=DayIterator.DayINOLPriority
            ListOfExercises.append(ExerciseClass.DailyExercise(weekindex, Day.Name, findExercise(exercise), week.Volume, week.Intensity, week.INOL_Target, DayINOLSetting))
            #warmup generation, depending on the setting
            if findExercise(exercise).generateWarmup:
                ListOfExercises.extend(Warmup.GenerateWarmup(ListOfExercises[-1]))

#DataFrame implementation        
path=f"{os.getcwd()}/Output.xlsx"
Program=DataFrame(data={"Week":[], "Day":[], "Exercise":[], "Sets":[], "Reps":[], "PercentageOfOneRepMax":[], "INOL":[]})
for index, exercise in enumerate(ListOfExercises):
    Program=concat([Program, 
                    DataFrame([[exercise.WeekIndex,
                                exercise.Day,
                                exercise.Name,
                                exercise.NumberOfSets, 
                                exercise.NumberOfReps,
                                exercise.Intensity,
                                exercise.INOL ]],
                            columns=Program.columns)],
                    ignore_index=True)
####################################################

#Excel file generation
Writer=ExcelWriter(path, "xlsxwriter")
Book=Writer.book
Default_Format=Book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})

if generateExcelOutput:
    #Excel output of the Program:
    my_index_cols = ["Day", "Exercise"]
    Program.set_index(my_index_cols).to_excel(Writer, sheet_name="Program", index=True, header=True, merge_cells=True)

    #formatting so that people don't have to set column widths every time they regenerate the program   
    for index, worksheet in enumerate(Book.worksheets()):
        for i, col in enumerate(Program.columns):
            if max(Program[col].astype(str).str.len()) >= len(Program.columns[i]):
                max_len=max(Program[col].astype(str).str.len())+2
            else:
                max_len = len(Program.columns[i])  + 2
            worksheet.set_column(i, max_len)
if generateWorkoutLog:
    #Output of WorkoutLog Sheet for tracking the completion of the program
    WorkoutLog=DataFrame(data={"DateTime":[], "Exercise":[], "Sets":[], "Reps":[], "Weight":[], "OneRepMax":[], "RPE":[], "INOL":[]})
    WorkoutLog.to_excel(Writer, sheet_name="WorkoutLog", index=False, header=True)
    for index, worksheet in enumerate(Book.worksheets()):
        if (index == 1 ): 
            INOL_formula = '=([Sets]*[Reps])/(100-([Weight]/[OneRepMax])*100)'
            Timestamp_formula = '=IF([Exercise]<>"",IF([DateTime]="",NOW(),[DateTime]),"")'
            OneRM_formula = '=IF([RPE]<>"",[Weight]/(1.0278-(0.0278*([Reps]+10-[RPE]))),[Weight]/(1.0278-(0.0278*([Reps]))))'
            datetime_format=Book.add_format({'num_format':'mmm d yyyy hh:mm AM/PM'})

            worksheet.add_table('A1:I2', {'columns': [{'header': 'DateTime',
                                                    'formula': Timestamp_formula,
                                                    'format': datetime_format},
                                                    {'header': 'Exercise'},
                                                    {'header': 'Sets'},
                                                    {'header': 'Reps'},
                                                    {'header': 'Weight'},
                                                    {'header': 'OneRepMax'},
                                                    {'header': 'RPE'},
                                                    {'header': 'INOL',
                                                    'formula':INOL_formula},
                                                    {'header': 'EstimateOneRM',
                                                    'formula': OneRM_formula}
                                                    ]})
Writer.close()
####################################################
