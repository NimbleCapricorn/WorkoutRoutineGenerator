import os
from prettytable import PrettyTable
from prettytable import ORGMODE, MARKDOWN, DEFAULT
from prettytable.colortable import ColorTable, Themes
import math
from Difficulty import *
from WeekClass import *
from ExerciseListDividerFunctions import *
from ExerciseClass import *
from copy import *
from ProgramDataStructure import *
from tablib import *
from xlsxwriter import *
from pandas import *

#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
####TODO#### this list should be checked: does every name exist?
ProgramExerciseList=["snatch", "snatch pull", "snatch balance", "clean", "clean pull", "front squat", "snatch", "snatch pull", "snatch balance", "jerk", "push press", "squat"]

Days=["Monday", "Tuesday", "Wednesday", "Friday"]

#Not advised weekly setting pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
Weeks=[Week(Volume.LOW, Intensity.MOD, INOL_Target.Deload), Week(Volume.MED, Intensity.MOD, INOL_Target.DailyRecoverable), Week(Volume.MED, Intensity.MODP, INOL_Target.LoadAccumulating), Week(Volume.MED, Intensity.LIGHT, INOL_Target.Deload)] 

#Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) 


#Create the program data
WeeksOfProgram:ProgramWeek=[]
DaysOfProgram:ProgramDay=[]
ListOfTheDaysExercises:DailyExercise=[]
for index, week in enumerate(Weeks):
    for Day in Days:
        for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
            ListOfTheDaysExercises.append(DailyExercise(exercise, week.volume, week.intensity, week.INOL_Target))
        DaysOfProgram.append(ProgramDay(Day, deepcopy(ListOfTheDaysExercises)))
        ListOfTheDaysExercises.clear()
    WeeksOfProgram.append(ProgramWeek(index, deepcopy(DaysOfProgram))) 
    DaysOfProgram.clear()

#for week in WeeksOfProgram: here for debugging purposes, and to show how to iterate through each exercise
#    for day in week.ProgramDays:
#        for exercise in day.ExerciseList:
#            print(exercise)


#Create a table with the days and exercises with the exerciselist subsets
DailyTableList=[]
WeeklyTable=PrettyTable()
WeeklyTable.set_style(ORGMODE)
WeeklyTable.field_names=Days
for week in WeeksOfProgram:
    for day in week.ProgramDays:
        DailyTable = PrettyTable()
        DailyTable.set_style(ORGMODE)
        DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax","INOL"]
        for index, exercise in enumerate(day.ExerciseList):
            DailyTable.add_row([exercise.Name, exercise.NumberOfSets, exercise.NumberOfReps, exercise.Intensity, exercise.INOL])
            if(index % windowsize == windowsize - 1 or index==len(day.ExerciseList)-1):
                #print(DailyTable)  only here for debugging purposes          
                DailyTableList.append(deepcopy(DailyTable))
                DailyTable.clear_rows()
    WeeklyTable.add_row(DailyTableList)
    DailyTableList.clear()
print(WeeklyTable)

#DataFrame implementation        
path=f"{os.getcwd()}/Output.xlsx"
DayDictionary={}
WeekDictionary={}
for weekindex, week in enumerate(WeeksOfProgram):
    OneWeek=[]
    for day in week.ProgramDays:
        OneDay=DataFrame(data={"Exercise":[], "Sets":[], "Reps":[], "PercentageOfOneRepMax":[], "INOL":[]})
        for index, exercise in enumerate(day.ExerciseList):
            OneDay.loc[index]=[exercise.Name, exercise.NumberOfSets, exercise.NumberOfReps, exercise.Intensity, exercise.INOL]
            if(index % windowsize == windowsize - 1 or index==len(day.ExerciseList)-1):
                if day.Name not in DayDictionary.keys():          
                    DayDictionary[day.Name]=(deepcopy(OneDay))
        OneWeek.append(deepcopy(DayDictionary))
        DayDictionary.clear()
        WeekDictionary[week.ID]=(deepcopy(OneWeek))


Writer=ExcelWriter(path, "xlsxwriter")
for index, week in enumerate(Weeks):
    for dayindex, day in enumerate(Days):
            WeekDictionary[index][dayindex][day].to_excel(Writer, sheet_name=f"Week {index}")