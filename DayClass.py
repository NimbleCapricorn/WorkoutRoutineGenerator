from dataclasses import dataclass
import csv

@dataclass
class DayClass:
    name:str
    DayINOLPriority:float

#Reading the users settings
DaySettingList:DayClass=[]
with open("Days.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=",")
    
    for row in reader:
        newDay = DayClass(str(row[0]), float(row[1]))
        DaySettingList.append(newDay)