from dataclasses import *
@dataclass
class Exercise:
   name:str
   minRepetitions:int
   maxRepetitions:int 
   def __str__(self):
       return f"{1}".format(self.name)    

@dataclass
class DailyExercise(Exercise):
    
    def __init__(self, name, minRepetitions, maxRepetitions, percentageOfOneRepMax, Sets, Reps):
        Exercise.__init__(name, minRepetitions,maxRepetitions)
        self.percentageOfOneRepMax=percentageOfOneRepMax
        self.Sets=Sets
        self.Reps=Reps