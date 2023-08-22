from dataclasses import dataclass
from ExerciseClass import *
@dataclass
class WorkoutDay:
    Exerciselist:DailyExercise = []
    def addExercise(self, DailyExercise):
        self.Exerciselist.append(DailyExercise)
        
class Week:
    days:WorkoutDay=[]
    def __init__(self, numberOfDays, days):
        for i in range(0,numberOfDays):
            self.days.append(WorkoutDay())


