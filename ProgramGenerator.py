from prettytable import PrettyTable
from prettytable import ORGMODE, MARKDOWN, DEFAULT
from prettytable.colortable import ColorTable, Themes
import math
from Difficulty import *
from WeekClass import *
from ExerciseListDividerFunctions import *
from CreateExerciseRow import *
from ExerciseClass import *
import copy
from ProgramDataStructure import *

#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
####TODO#### this list should be checked: does every name exist?
ProgramExerciseList=["snatch", "clean and jerk", "clean pull", "squat", "OHP", "push press", "squat"]

Days=["Monday", "Tuesday", "Wednesday", "Friday"]

#Not advised weekly setting pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
Weeks=[Week(Volume.LOW, Intensity.LIGHT, INOL_Target.Deload), Week(Volume.MED, Intensity.HEAVYP, INOL_Target.DailyRecoverable)] 

#Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) 


#Create the program data
WeeksOfProgram:ProgramWeek=[]
DaysOfProgram:ProgramDay=[]
ListOfTheDaysExercises:DailyExercise=[]
for index, week in enumerate(Weeks):
    for Day in Days:
        for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
            ListOfTheDaysExercises.append(DailyExercise(*createExerciseRow(exercise, week.volume, week.intensity, week.INOL_Target)))
        DaysOfProgram.append(ProgramDay(Day, copy.deepcopy(ListOfTheDaysExercises)))
        ListOfTheDaysExercises.clear()
    WeeksOfProgram.append(ProgramWeek(index, copy.deepcopy(DaysOfProgram))) 
    DaysOfProgram.clear()

#for week in WeeksOfProgram: here for debugging purposes, and to show how to iterate through each exercise
#    for day in week.ProgramDays:
#        for exercise in day.ExerciseList:
#            print(exercise)


#Create a table with the days and exercises with the exerciselist subsets using either the sliding window or the chunks 
DailyTableList=[]
WeeklyTable=PrettyTable()
WeeklyTable.set_style(DEFAULT)
WeeklyTable.field_names=Days
for week in WeeksOfProgram:
    for day in week.ProgramDays:
        DailyTable = PrettyTable()
        DailyTable.set_style(DEFAULT)
        DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax","INOL"]
        for index, exercise in enumerate(day.ExerciseList):
            DailyTable.add_row([exercise.Name, exercise.NumberOfSets, exercise.NumberOfReps, exercise.Intensity, exercise.INOL])
            if(index % windowsize == windowsize - 1 or index==len(day.ExerciseList)-1):
                #print(DailyTable)  only here for debugging purposes          
                DailyTableList.append(copy.deepcopy(DailyTable))
                DailyTable.clear_rows()
    WeeklyTable.add_row(DailyTableList)
    DailyTableList.clear()
print(WeeklyTable)

#The output file below is experimental and does not produce an accurate result
with open('Output.html', 'w') as output_file:
    output_file.write(WeeklyTable.get_html_string(format=True))              
with open('Output.txt', 'w') as outpul_file:
    outpul_file.write(WeeklyTable.get_formatted_string())