from prettytable import PrettyTable
from prettytable import ORGMODE, MARKDOWN
from prettytable.colortable import ColorTable, Themes
import math
from Difficulty import *
from WeekClass import *
from ExerciseListDividerFunctions import *
from CreateExerciseRow import *
from ExerciseClass import *
import copy

#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
####TODO#### this list should be checked: does every name exist?
ProgramExerciseList=["snatch", "clean and jerk", "clean pull", "squat", "OHP", "push press", "squat"]

Days=["Monday", "Tuesday", "Wednesday", "Friday"]

#Not advised weekly setting pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
Weeks=[Week(Volume.LOW, Intensity.LIGHT, INOL_Target.Deload), Week(Volume.MED, Intensity.HEAVYP, INOL_Target.DailyRecoverable)] 

#Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) 


#Create the program data
TemporaryDailyExerciseList:DailyExercise=[]
WeeklyCollectionOfDailyExercises=[]
for week in Weeks:
    for Day in Days:
        for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
            TemporaryDailyExerciseList.append(DailyExercise(*createExerciseRow(exercise, week.volume, week.intensity, week.INOL_Target)))        
    WeeklyCollectionOfDailyExercises.append(copy.deepcopy(TemporaryDailyExerciseList))
    TemporaryDailyExerciseList.clear()
#for DailyExerciseCollection in WeeklyCollectionOfDailyExercises: (only here for debugging purposes)
#    for DailyExerciseRows in DailyExerciseCollection:
#        print(DailyExerciseRows) 


#Create a table with the days and exercises with the exerciselist subsets using either the sliding window or the chunks 
DailyTableList=[]
WeeklyTable=PrettyTable()
WeeklyTable.set_style(MARKDOWN)
WeeklyTable.field_names=Days
for DailyExerciseCollection in WeeklyCollectionOfDailyExercises:
    DailyTable = PrettyTable()
    DailyTable.set_style(MARKDOWN)
    DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax","INOL"]
    for index, DailyExerciseRows in enumerate(DailyExerciseCollection):
        DailyTable.add_row((DailyExerciseRows.Name, DailyExerciseRows.NumberOfSets, DailyExerciseRows.NumberOfReps, DailyExerciseRows.Intensity, DailyExerciseRows.INOL))
        if(index % windowsize == windowsize - 1 or index==len(DailyExerciseCollection)-1):
            #print(DailyTable) only here for debugging purposes               
            DailyTableList.append(copy.deepcopy(DailyTable))
            DailyTable.clear_rows()
    WeeklyTable.add_row(DailyTableList)
    DailyTable.clear()
    DailyTableList.clear()
print(WeeklyTable) #If ran from the command line, and only needing it for a quick picture, uncomment this line

#The output file below is experimental and does not produce an accurate result
with open('Output.html', 'w') as output_file:
    output_file.write(WeeklyTable.get_html_string(format=True))              
