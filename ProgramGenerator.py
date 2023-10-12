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
    ProgramExerciseList=ProgramConfig['ProgramExerciseList']
    Days=ProgramConfig['Days']
    Weeks=[]
    for WeekConfigItem in ProgramConfig['Weeks']:
        VolumeSetting=searchVolumeSetting(WeekConfigItem['Volume'])
        IntensitySetting=searchIntensitySetting(WeekConfigItem['Intensity'])
        INOL_TargetSetting=searchINOLSetting(WeekConfigItem['INOL_Target'])
        Weeks.append(Week(VolumeSetting, IntensitySetting, INOL_TargetSetting))

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

#formatting so that people don't have to set column widths every time they regenerate the program   
for index, worksheet in enumerate(Book.worksheets()):
    for i, col in enumerate(OneWeek.columns):
        if max(WeekList[index][col].astype(str).str.len()) >= len(WeekList[index].columns[i]):
            max_len=max(WeekList[index][col].astype(str).str.len())+1
        else:
            max_len = len(WeekList[index].columns[i])  + 1
        worksheet.set_column(i, i, max_len)

#Merging cells based on headers for less visual clutter
#TODO# (logically it should work but can't merge a range and then turn it into a table)
merge_range=False #debugging tool
merge_tags=["Exercise"]
if merge_range:
    for merge_tag in merge_tags:
        for weekindex, week in enumerate(WeekList):
            startCells = [1]
            for row in range(2,len(week)+1):
                if (week.loc[row-1,merge_tag] != week.loc[row-2,merge_tag]):
                    startCells.append(row)
            lastRow = len(week)
            merge_format = Book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
            worksheet = Writer.sheets[f'Week {weekindex+1}']

            for row in startCells:
                try:
                    endRow = startCells[startCells.index(row)+1]-1
                    if row == endRow:
                        worksheet.write(row, 0, week.loc[row-1,merge_tag], merge_format)
                    else:
                        worksheet.merge_range(row, 0, endRow, 0, week.loc[row-1,merge_tag], merge_format)
                except IndexError:
                    if row == lastRow:
                        worksheet.write(row, 0, week.loc[row-1,merge_tag], merge_format)
                    else:
                        worksheet.merge_range(row, 0, lastRow, 0, week.loc[row-1,merge_tag], merge_format)
Pivot_table=True
if Pivot_table:
    my_index_cols = ["Day", "Exercise"] # this can also be a list of multiple columns
    for week in WeekList:
        week.set_index(my_index_cols).to_excel('filename.xlsx', index=True, header=True, merge_cells=True)




#Output of WorkoutLog Sheet for tracking the completion of the program
WorkoutLog=DataFrame(data={"DateTime":[], "Exercise":[], "Sets":[], "Reps":[], "Weight":[], "OneRepMax":[], "RPE":[], "INOL":[]})
WorkoutLog.to_excel(Writer, sheet_name="WorkoutLog", index=False, header=True)
for index, worksheet in enumerate(Book.worksheets()):
    if (index < len(Weeks) ):
        worksheet.add_table(f'A1:F50', {'columns': [{'header': 'Day'},
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