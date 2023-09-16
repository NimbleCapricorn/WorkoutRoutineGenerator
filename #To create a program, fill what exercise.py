from prettytable import PrettyTable
#To create a program, fill what exercises you want to do, and what days of the week you want to work out on
ExerciseList=["santch", "clean and jerk","clean pull","squat","OHP"]
Days=["hétfő","kedd", "csütörtök", "péntek"]
#Create a table with the days and exercises
for Day in Days:
    DailyTable = PrettyTable()
    DailyTable.field_names=["Exercise", "Sets", "Reps", "PercentageOfOneRepMax"]
    for Exercise in ExerciseList:
        if ExerciseList.index(Exercise) <= (len(ExerciseList) / len(Days)):
            DailyTable.add_row([Exercise, 3, 3, 70])
    print(DailyTable)       
            
