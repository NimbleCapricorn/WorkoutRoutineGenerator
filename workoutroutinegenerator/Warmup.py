from .exerciseclass import ExerciseClass
from .exerciseclass.difficulty.Difficulty import IntensityList
from copy import deepcopy

#warmup generation
class Warmup(ExerciseClass.DailyExercise):
    WeekIndex:int=[]
    Day:str=[]
    Name:str=[]
    NumberOfSets:int=[]
    NumberOfReps:int=[]
    Intensity:float=[]
    INOL:float=[]
    NumberOfWarmupSets:int=4

    def __init__(self, ParentExercise:ExerciseClass.DailyExercise):
        self.WeekIndex.clear()
        self.Day.clear()
        self.Name.clear()
        self.NumberOfSets.clear()
        self.NumberOfReps.clear()
        self.Intensity.clear()
        self.INOL.clear()
        
        WarmupIntensity=IntensityList[6] #LightPIntensity
        for iterator in range(0, self.NumberOfWarmupSets, 1):
            self.WeekIndex.append(ParentExercise.WeekIndex)
            self.Day.append(ParentExercise.Day)
            self.Name.append(ParentExercise.Name)
            self.NumberOfSets.append(1)
            self.NumberOfReps.append((self.NumberOfWarmupSets-iterator))
            self.Intensity.append(round(WarmupIntensity.IntensityFunction(self.NumberOfReps[-1]), 1))
            self.INOL.append(round(self.calculateINOL(self.NumberOfSets[-1], self.NumberOfReps[-1], self.Intensity[-1]), 1))

    def getWarmupExercises(self):
        WarmupExerciseList:ExerciseClass.DailyExercise=[]
        for iterator in range(0, self.NumberOfWarmupSets, 1):
            WarmupExerciseList.append(deepcopy(ExerciseClass.DailyExercise.from_args(self.WeekIndex[iterator], self.Day[iterator], self.Name[iterator], self.NumberOfSets[iterator], self.NumberOfReps[iterator], self.Intensity[iterator], self.INOL[iterator])))
        return WarmupExerciseList 
        
def GenerateWarmup(CallingExercise:ExerciseClass.DailyExercise):
    WarmupSets:ExerciseClass.DailyExercise=[]
    WarmupExercises=Warmup(CallingExercise)
    WarmupSets.extend(WarmupExercises.getWarmupExercises())
        
    return WarmupSets