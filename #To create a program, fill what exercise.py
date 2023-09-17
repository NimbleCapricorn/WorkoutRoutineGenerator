from prettytable import PrettyTable
import math
#To create a program, fill what exercises you want to do, and what days of the week you want to work out on
ExerciseList=["santch", "clean and jerk","clean pull","squat","OHP"]
Days=["hétfő","kedd", "csütörtök", "péntek"]
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
windowsize = math.ceil(len(ExerciseList)/len(Days))
#Create a table with the days and exercises with sliding window
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
