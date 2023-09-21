from dataclasses import *
import csv

@dataclass
class Exercise:
   Name:str
   minRepetitions:int
   maxRepetitions:int 
   def __str__(self):
       return f"{self.Name}"    

#read exercises
ExerciseList:Exercise=[]
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = Exercise(str(row[0]), int(row[1]), int(row[2]))
        ExerciseList.append(newExercise)
