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

#Output setup: do you need a simple txt output?
txt_output=False
#Input setup: do you use the yaml config or the script inline config?
yaml_config=True
if yaml_config:
    with open('ProgramConfig.yml', 'r') as file:
        ProgramConfig = safe_load(file)
        ProgramExerciseList=ProgramConfig['ProgramExerciseList']
        Days=ProgramConfig['Days']
        Weeks=[]
        for WeekConfigItem in ProgramConfig['Weeks']:
            VolumeSetting=searchVolumeSetting(WeekConfigItem['Volume'])
            IntensitySetting=searchIntensitySetting(WeekConfigItem['Intensity'])
            INOL_TargetSetting=searchINOLSetting(WeekConfigItem['INOL_Target'])
            Weeks.append(Week(VolumeSetting, IntensitySetting, INOL_TargetSetting))

if not yaml_config:
    #To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
    ProgramExerciseList=["snatch", "snatch pull", "snatch balance", "clean", "clean pull", "front squat", "snatch", "snatch pull", "snatch balance", "jerk", "push press", "squat"]

    Days=["Monday", "Tuesday", "Wednesday", "Friday"]

    #Not advised weekly setting pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
    Weeks=[Week(Volume.LOW, Intensity.MOD, INOL_Target.Deload), Week(Volume.MED, Intensity.MOD, INOL_Target.DailyRecoverable), Week(Volume.MED, Intensity.MODP, INOL_Target.DailyRecoverable), Week(Volume.MED, Intensity.LIGHT, INOL_Target.Deload)] 

#Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) 


#Create the program data
WeeksOfProgram:ProgramWeek=[]
DaysOfProgram:ProgramDay=[]
ListOfTheDaysExercises:DailyExercise=[]
DayINOLSetting:float
for index, week in enumerate(Weeks):
    for Day in Days:
        for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
            #generate the working sets:
            for DayIterator in DaySettingList: 
                if DayIterator.name == Day: 
                    DayINOLSetting=DayIterator.DayINOLPriority
            ListOfTheDaysExercises.append(DailyExercise(exercise, week.Volume, week.Intensity, week.INOL_Target, DayINOLSetting))
            #warmup generation, depending on the 
            ListOfTheDaysExercises.extend(GenerateWarmup(ListOfTheDaysExercises[-1]))
        DaysOfProgram.append(ProgramDay(Day, deepcopy(ListOfTheDaysExercises)))
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
Format=Book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 2})
for weekindex, week in enumerate(WeekList):
    week.to_excel(Writer, sheet_name=f"Week {weekindex+1}", index=False, header=True, merge_cells=True)

#Output of WorkoutLog Sheet
WorkoutLog=DataFrame(data={"DateTime":[], "Exercise":[], "Sets":[], "Reps":[], "Weight":[], "OneRepMax":[], "RPE":[], "INOL":[]})
WorkoutLog.to_excel(Writer, sheet_name="WorkoutLog", index=False, header=True)
for index, worksheet in enumerate(Book.worksheets()):
    if (index < len(Weeks)):
        worksheet.add_table(f'A1:F100', {'columns': [{'header': 'Day'},
                                                                              {'header': 'Exercise'},
                                                                              {'header': 'Sets'},
                                                                              {'header': 'Reps'},
                                                                              {'header': 'PercentageOfOneRepMax'},
                                                                              {'header': 'INOL'},
                                                                             ]})
    else:
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