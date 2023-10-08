from ExerciseClass import *
from Difficulty import *
from copy import deepcopy
#warmup generation
class Warmup(DailyExercise):
    Name:str=[]
    NumberOfSets:int=[]
    NumberOfReps:int=[]
    Intensity:float=[]
    INOL:float=[]
    NumberOfWarmupSets:int=4

    def __init__(self, ParentExercise:DailyExercise):
        self.Name.clear()
        self.NumberOfSets.clear()
        self.NumberOfReps.clear()
        self.Intensity.clear()
        self.INOL.clear()
        
        WarmupIntensity=IntensityList[6] #LightPIntensity
        for iterator in range(0, self.NumberOfWarmupSets, 1):
            self.Name.append(ParentExercise.Name)
            self.NumberOfSets.append(1)
            self.NumberOfReps.append((self.NumberOfWarmupSets-iterator))
            self.Intensity.append(round(WarmupIntensity.IntensityFunction(self.NumberOfReps[-1]), 1))
            self.INOL.append(round(self.calculateINOL(self.NumberOfSets[-1], self.NumberOfReps[-1], self.Intensity[-1]), 1))

    def getWarmupExercises(self):
        WarmupExerciseList:DailyExercise=[]
        for iterator in range(0, self.NumberOfWarmupSets, 1):
            WarmupExerciseList.append(deepcopy(DailyExercise.from_args(self.Name[iterator], self.NumberOfSets[iterator], self.NumberOfReps[iterator], self.Intensity[iterator], self.INOL[iterator])))
        return WarmupExerciseList 
        
def GenerateWarmup(CallingExercise:DailyExercise):
    temporaryExercise:Exercise
    WarmupSets:DailyExercise=[]
    #check which exercise it is, so you can figure our whether you need to generate warmup
    for ExerciseIterator in ExerciseList: 
        if ExerciseIterator.Name == CallingExercise.Name: 
             temporaryExercise=ExerciseIterator
    if temporaryExercise.generateWarmup:
        WarmupExercises=Warmup(CallingExercise)
        WarmupSets.extend(WarmupExercises.getWarmupExercises())
        
    return WarmupSets