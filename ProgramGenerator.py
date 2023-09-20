from prettytable import PrettyTable
import math
from Difficulty import *
from WeekClass import *
from ExerciseListDividerFunctions import *
from CreateExerciseRow import *
from ExerciseClass import *

#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
ProgramExerciseList=["snatch", "clean and jerk", "clean pull", "squat", "OHP", "push press", "squat"] ####TODO#### this list should be checked: does every name exist?
Days=["Monday", "Tuesday", "Wednesday", "Friday"]
Weeks=[Week(Volume.LOW,"LIGHT"), Week(Volume.MED,"MAX")] #Not advised pairings are HIGH volume with MODP and up intensity (except for enhanced athletes), LOW volume with MOD and down intensity (only for deloads)
windowsize = math.ceil(len(ProgramExerciseList)/len(Days)) #Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal parts
bool_SlidingWindow=False #Set this if you would like to use sliding window instead of only doing each exercise once per mention in the list

#Create a table with the days and exercises with the exerciselist subsets using either the sliding window or the chunks
for week in Weeks:
    for Day in Days:
        DailyTable = PrettyTable()
        DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax"]
        if(bool_SlidingWindow):
            for exercise in tuple(sliding_window(ProgramExerciseList, windowsize))[Days.index(Day)]:
                DailyTable.add_row(createExerciseRow(exercise, week.volume, week.intensity))
        else:
            for exercise in tuple(divide_chunks(ProgramExerciseList, windowsize))[Days.index(Day)]:
                DailyTable.add_row(createExerciseRow(exercise, week.volume, week.intensity))        
        print(DailyTable)               
