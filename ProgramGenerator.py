from prettytable import PrettyTable
import math
from Difficulty import *
from WeekClass import *
from ExerciseListDividerFunctions import *
from CreateExerciseRow import *
from ExerciseClass import *
from prettytable import ORGMODE

#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
####TODO#### this list should be checked: does every name exist?
ProgramExerciseList=["snatch", "clean and jerk", "clean pull", "squat", "OHP", "push press", "squat"]

Days=["Monday", "Tuesday", "Wednesday", "Friday"]

#Not advised weekly setting pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
Weeks=[Week(Volume.LOW, Intensity.LIGHT, INOL_Target.Deload), Week(Volume.MED, Intensity.HEAVYP, INOL_Target.DailyRecoverable)] 

#Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) 

#Set this if you would like to use sliding window instead of only doing each exercise once per mention in the list
bool_SlidingWindow=False 

#Create a table with the days and exercises with the exerciselist subsets using either the sliding window or the chunks
DailyTableList=[]
WeeklyTable=PrettyTable()
WeeklyTable.field_names=Days
for week in Weeks:
    for Day in Days:
        DailyTable = PrettyTable()
        DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax","INOL"]
        if(bool_SlidingWindow):
            for exercise in tuple(sliding_window(ProgramExerciseList, windowsize))[Days.index(Day)]:
                DailyTable.add_row(createExerciseRow(exercise, week.volume, week.intensity, week.INOL_Target))
        else:
            for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
                DailyTable.add_row(createExerciseRow(exercise, week.volume, week.intensity, week.INOL_Target))        
        DailyTableList.append(DailyTable)
    WeeklyTable.add_row(DailyTableList)
    DailyTableList.clear()
WeeklyTable.set_style(ORGMODE)
print(WeeklyTable)               
