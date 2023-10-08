from ExerciseClass import *
from Difficulty import *
#warmup generation
class Warmup(DailyExercise):
    limitIntensity:float
    Name:str=[]
    NumberOfSets:int=[]
    NumberOfReps:int=[]
    Intensity:float=[]
    INOL:float=[]
    def __init__(self, ParentExercise:DailyExercise):
        NumberOfWarmupSets:int=4
        self.limitIntensity=ParentExercise.Intensity
        WarmupIntensity=IntensityList[5] #LightPIntensity
        for iterator in range(0, NumberOfWarmupSets-1, 1):
            self.Name.append(ParentExercise.Name)
            self.NumberOfSets.append(1)
            self.NumberOfReps.append(NumberOfWarmupSets-iterator)
            self.Intensity.append(round(WarmupIntensity.IntensityFunction(self.NumberOfReps[-1]), 1))
            self.INOL.append(round(self.calculateINOL(self.NumberOfSets[-1], self.NumberOfReps[-1], self.Intensity[-1]), 1))

    def getWarmupExercises(self):
        WarmupExerciseList:DailyExercise=[]
        NotUsedLastParameter:str=[]
        for iterator in range(len(self.Name)):
            WarmupExerciseList.append(DailyExercise.from_args(self.Name[iterator], self.NumberOfSets[iterator], self.NumberOfReps[iterator], self.Intensity[iterator], self.INOL[iterator]))
        return WarmupExerciseList
        
def GererateWarmup(DailyExercise:DailyExercise):
    temporaryExercise:Exercise  #for warmup generation
    #check which exercise it is, so you can figure our whether you need to generate warmup
    for ExerciseIterator in ExerciseList: 
        if ExerciseIterator.Name == exercise: 
             temporaryExercise=ExerciseIterator
                #if you need warmup generation, generate it:
    if temporaryExercise.generateWarmup:
        WarmupSets=Warmup(ListOfTheDaysExercises[-1])
        ListOfTheDaysExercises.extend(deepcopy(WarmupSets.getWarmupExercises()))
        WarmupSets=None