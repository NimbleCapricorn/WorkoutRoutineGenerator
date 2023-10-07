from ExerciseClass import *
from Difficulty import *
#warmup generation
class Warmup(DailyExercise):
    limitIntensity:float
    NumberOfSets:int=[]
    NumberOfReps:int=[]
    Intensity:float=[]
    INOL:float=[]
    def __init__(self, ParentExercise:DailyExercise):
        NumberOfWarmupSets:int=4
        self.Name=ParentExercise.Name
        self.limitIntensity=ParentExercise.Intensity
        WarmupIntensityFunction=IntensityList[5] #LightPIntensity
        for iterator in range(1, NumberOfWarmupSets, 1):
            self.NumberOfSets[iterator]=1
            self.NumberOfReps[iterator]=NumberOfWarmupSets-iterator
            self.Intensity[iterator]=round(WarmupIntensityFunction(self.NumberOfReps),1)
            self.INOL[iterator]=round(self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity),1)
    
        

