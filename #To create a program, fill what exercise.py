from prettytable import PrettyTable
import math
from Difficulty import *
from WeekClass import *
#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are volume-intensity pairs
ExerciseList=["snatch", "clean and jerk", "clean pull", "squat", "OHP","PushPress","squat"]
Days=["Monday", "Tuesday", "Wednesday", "Friday"]
Weeks=[Week(Volume.LOW,"LIGHT"), Week(Volume.MED,"LIGHTP")] #Not advised pairings are HIGH volume with MODP and up intensity, LOW volume with MED and down intensity (only for deloads)
windowsize = math.ceil(len(ExerciseList)/len(Days)) #Overwrite this to make other exercise groupings other than chunking up the ExerciseList into equal chunks
bool_SlidingWindow=False #Set this if you would like to use sliding window instead of only doing each exercise once

#functions and variables that make the generation easier
def sliding_window(array, k):
    """give back k size subarrays of array using a sliding window"""
    for i in range(len(array)-k+1):
        yield array[i:i+k]
def divide_chunks(l, n):
    """Yield successive n-sized chunks from l.""" 
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

#Create a table with the days and exercises with the exerciselist subsets using either the sliding window or the chunks
for Day in Days:
    DailyTable = PrettyTable()
    DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax"]
    if(bool_SlidingWindow):
        for Exercise in tuple(sliding_window(ExerciseList, windowsize))[Days.index(Day)]:
            DailyTable.add_row([Exercise, 3, 3, 70])
    else:
        for Exercise in tuple(divide_chunks(ExerciseList, windowsize))[Days.index(Day)]:
            DailyTable.add_row([Exercise, 3, 3, 70])        
    print(DailyTable)               
