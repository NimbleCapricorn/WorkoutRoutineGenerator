#!/usr/bin/env python3 
#this script requires python 3.10+, as match cases are only supported by those versions.
import os
import math
from Difficulty import *
from WeekClass import *
from DayClass import *
from ExerciseListDividerFunctions import *
from ExerciseClass import *
from copy import *
from ProgramDataStructure import *
from tablib import *
from xlsxwriter import *
from pandas import *
from subprocess import *
from yaml import *
from warmup import *

#configuration parsing
with open('ProgramConfig.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    ProgramSettingDays=[]
    for DayConfigItem in ProgramConfig['Days']:
        ProgramSettingDays.append(ProgramSettingDay(DayConfigItem['Name'], DayConfigItem['ExerciseList']))
    Weeks=[]
    for WeekConfigItem in ProgramConfig['Weeks']:
        VolumeSetting=searchVolumeSetting(WeekConfigItem['Volume'])
        IntensitySetting=searchIntensitySetting(WeekConfigItem['Intensity'])
        INOL_TargetSetting=searchINOLSetting(WeekConfigItem['INOL_Target'])
        Weeks.append(Week(VolumeSetting, IntensitySetting, INOL_TargetSetting))

#Create the program data
WeeksOfProgram:ProgramWeek=[]
DaysOfProgram:ProgramDay=[]
ListOfTheDaysExercises:DailyExercise=[]
DayINOLSetting:float
for index, week in enumerate(Weeks):
    for Day in ProgramSettingDays:
        for exercise in Day.ExerciseList:
            #generate the working sets:
            for DayIterator in DaySettingList: 
                if DayIterator.name == Day.Name: 
                    DayINOLSetting=DayIterator.DayINOLPriority
            ListOfTheDaysExercises.append(DailyExercise(exercise, week.Volume, week.Intensity, week.INOL_Target, DayINOLSetting))
            #warmup generation, depending on the 
            ListOfTheDaysExercises.extend(GenerateWarmup(ListOfTheDaysExercises[-1]))
        DaysOfProgram.append(ProgramDay(Day.Name, deepcopy(ListOfTheDaysExercises)))
        ListOfTheDaysExercises.clear()
    WeeksOfProgram.append(ProgramWeek(index, deepcopy(DaysOfProgram))) 
    DaysOfProgram.clear()


#DataFrame implementation        
path=f"{os.getcwd()}/Output.xlsx"
WeekList=[]
for weekindex, week in enumerate(WeeksOfProgram):
    OneWeek=DataFrame(data={"Day":[], "Exercise":[], "Sets":[], "Reps":[], "PercentageOfOneRepMax":[], "INOL":[]})
    for dayindex, day in enumerate(week.ProgramDays):
        for index, exercise in enumerate(day.ExerciseList):
            OneWeek=concat([OneWeek, DataFrame([[day.Name, exercise.Name, exercise.NumberOfSets, exercise.NumberOfReps, exercise.Intensity, exercise.INOL ]], columns=OneWeek.columns)], ignore_index=True)
    WeekList.append(deepcopy(OneWeek))


Writer=ExcelWriter(path, "xlsxwriter")
Book=Writer.book
#Output of the Program:
Default_Format=Book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
my_index_cols = ["Day", "Exercise"]
for weekindex, week in enumerate(WeekList):
    week.set_index(my_index_cols).to_excel(Writer, sheet_name=f"Week {weekindex+1}", index=True, header=True, merge_cells=True)

#formatting so that people don't have to set column widths every time they regenerate the program   
for index, worksheet in enumerate(Book.worksheets()):
    for i, col in enumerate(OneWeek.columns):
        if max(WeekList[index][col].astype(str).str.len()) >= len(WeekList[index].columns[i]):
            max_len=max(WeekList[index][col].astype(str).str.len())+2
        else:
            max_len = len(WeekList[index].columns[i])  + 2
        worksheet.set_column(i, i, max_len)

#Output of WorkoutLog Sheet for tracking the completion of the program
WorkoutLog=DataFrame(data={"DateTime":[], "Exercise":[], "Sets":[], "Reps":[], "Weight":[], "OneRepMax":[], "RPE":[], "INOL":[]})
WorkoutLog.to_excel(Writer, sheet_name="WorkoutLog", index=False, header=True)
for index, worksheet in enumerate(Book.worksheets()):
    if (index >= len(Weeks) ): 
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