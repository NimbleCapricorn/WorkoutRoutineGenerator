from prettytable import PrettyTable
import math
import Difficulty
#To create a program, fill what exercises you want to do, and what days of the week you want to work out on. Weeks are intensity-volume pairs
ExerciseList=["santch", "clean and jerk","clean pull","squat","OHP"]
Days=["hétfő","kedd", "csütörtök", "péntek"]
Weeks=[]
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
#Intensity functions to make generating varying intensity weeks easier
MaxIntensity=Difficulty.IntensityFunction("Max", [-0.0405, 0.6583, -5.776, 104.87])
HeavyPIntensity=Difficulty.IntensityFunction("Heavy+", [-0.0049, +0.1003, -3.411, 97.711])
HeavyIntensity=Difficulty.IntensityFunction("Heavy", [-0.01, + 0.1733, -0.4844, 92.825])
ModPIntensity=Difficulty.IntensityFunction("Mod+", [-0.0124, + 0.2095, - 0.2897, 82.753])
ModIntensity=Difficulty.IntensityFunction("Mod", [-0.0131, 0.2206, -0.1739, 77.707])
LightPIntensity=Difficulty.IntensityFunction("Light+",[-0.0124, 0.2095, -0.2897, 82.753])
LightIntensity=Difficulty.IntensityFunction("Light",[-0.0143, 0.2387, -0.0766, 72.67])
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
