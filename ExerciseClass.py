from dataclasses import *
@dataclass
class Exercise:
   name:str
   minRepetitions:int
   maxRepetitions:int 
   def __str__(self):
       return f"{self.name}"    

#read exercises
ExerciseList=[]
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = Exercise(row[0], row[1], row[2])
        ExerciseList.append(newExercise)
        print(newExercise)
