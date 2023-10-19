from dataclasses import *
from yaml import *
from Difficulty import *
from ExerciseClass import *
from WeekClass import *
from copy import deepcopy

@dataclass
class Exercise:
   Name:str
   minRepetitions:int #minimum number or repetitions that can be prescribed in a set
   maxRepetitions:int #maximum number or repetitions that can be prescribed in a set
   Priority:float # float between 0.5 and 1 where 0.5 is the highest and 1 is the lowest. (0.5 means a 2x increase in INOL, so use sparingly)
   generateWarmup:bool
   def __str__(self):
       return f"{self.Name}"    

#import exercise settings   
with open('Exercises.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    ExerciseList=[]
    for ExerciseConfigItem in ProgramConfig['Exercises']:
        ExerciseList.append(Exercise(ExerciseConfigItem['Name'], ExerciseConfigItem['minRepetitions'], ExerciseConfigItem['maxRepetitions'], ExerciseConfigItem['Priority'], ExerciseConfigItem['generateWarmup']))

@dataclass
class DailyExercise:
    WeekIndex:int
    Day:str
    Name:str
    NumberOfSets:int
    NumberOfReps:int
    Intensity:float
    INOL:float

    def calculateINOL(self, setcount, temporaryReps, Intensity):
        return (setcount*temporaryReps)/(100-Intensity)
    
    def calculateErrorFromINOL(self, INOL, INOL_target):
        return ((INOL-INOL_target)/INOL_target)
    
    def SetNumberOfSets(self, VolumeSetting, LOWVolume:int, MEDVolume:int, HIGHVolume:int):
        match VolumeSetting.name:
            case Volume.LOW.name:
                self.NumberOfSets=LOWVolume
            case Volume.MED.name:
                self.NumberOfSets=MEDVolume
            case Volume.HIGH.name:
                self.NumberOfSets=HIGHVolume

    def SetNumberOfReps(self, Exercise:Exercise, NumberOfReps:int):
        FurtherChangesPossible:bool=False
        if NumberOfReps <= Exercise.maxRepetitions and NumberOfReps >= Exercise.minRepetitions:
            self.NumberOfReps=NumberOfReps
            FurtherChangesPossible=True
        elif NumberOfReps > Exercise.maxRepetitions:
            NumberOfReps = Exercise.maxRepetitions
            FurtherChangesPossible=False
        elif NumberOfReps < Exercise.minRepetitions:
            NumberOfReps = Exercise.minRepetitions
            FurtherChangesPossible=False
        return FurtherChangesPossible

    def __init__(self, weeknumber, day, name, VolumeSetting:Volume, IntensitySetting:Intensity, INOL_Target:INOL_Target, DayINOLSetting:float):
        #temporary values to make calcuations easier
        self.WeekIndex=weeknumber
        self.Day=day
        temporaryExercise:Exercise
        IntermittentIntensity:IntensityFunction
        self.NumberOfSets=VolumeSetting.value
        #find which exercise it is  ##TODO## what happens if we can't find the exercise?
        for ExerciseIterator in ExerciseList: 
            if ExerciseIterator.Name == name: 
                temporaryExercise=ExerciseIterator

        INOL_TargetWithPriority=INOL_Target.value/(temporaryExercise.Priority*DayINOLSetting)

        #determine best rep number for the volume setting
        match VolumeSetting.name: 
            case Volume.LOW.name:
                self.NumberOfReps=temporaryExercise.maxRepetitions
            case Volume.MED.name:
                self.NumberOfReps=round((temporaryExercise.maxRepetitions+temporaryExercise.minRepetitions)/2)
            case Volume.HIGH.name:
                self.NumberOfReps=temporaryExercise.minRepetitions



        #calculate intensity based on determined repcount and given intensity setting
        for IntensityIterator in IntensityList:
            if  IntensityIterator.name == IntensitySetting.name:
                IntermittentIntensity=IntensityIterator
        self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)

        self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity) #Intensity Plus Number Of Lifts is a common number to self-check a program.

        #Depending on the INOL target setting, to achieve a good stimulus, numbers may need to be bumped up or down as well   
        #Very big error: correct set count
        for iterator in range(1,2,1):
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) < (-0.4/iterator)):
                self.NumberOfSets+=1
                self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity)
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) > (0.4/iterator)): 
                self.NumberOfSets-=1 
                if self.NumberOfSets == 0:
                    self.NumberOfSets = 1
                    break
                self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity)
                

            #semi-big error: change rep number
            FurtherChangesPossible:bool=True
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) < (-0.14/iterator) ):
                if (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) < (-0.24/iterator) ):
                    FurtherChangesPossible=self.SetNumberOfReps(temporaryExercise, self.NumberOfReps+2)
                else:
                    FurtherChangesPossible=self.SetNumberOfReps(temporaryExercise, self.NumberOfReps+1)
                self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)
                if not FurtherChangesPossible:
                    break
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) > (0.2/iterator) ):
                FurtherChangesPossible=self.SetNumberOfReps(temporaryExercise, self.NumberOfReps-1)
                self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)
                if not FurtherChangesPossible:
                    break
            self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity)

            #small error:change intensity
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) < (- 0.1/iterator) ):
                self.Intensity+=0.3
                self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity)
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) > (0.1/iterator) ):
                self.Intensity-=0.3
                self.INOL=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity)
        
        self.Intensity=round(self.Intensity,1)
        self.INOL=round(self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity),1)
        
        self.Name=name

    @classmethod
    def from_args(cls, weekindex:int, day:str, name:str, NumberOfSets:int, NumberOfReps:int, intensity:float, INOL:float): 
        instance=cls(0, "Monday", "snatch", Volume.LOW, Intensity.MOD, INOL_Target.DailyRecoverable, 1.0) #these parameters are gonna be overwritten, but can't create new instance  without some data
        instance.WeekIndex=weekindex
        instance.Day=day
        instance.Name=name
        instance.NumberOfSets=NumberOfSets
        instance.NumberOfReps=NumberOfReps
        instance.Intensity=intensity
        instance.INOL=INOL
        return instance

    def __str__(self):
        return f"Exercise named:{self.Name}, number of sets:{self.NumberOfSets}, number of reps:{self.NumberOfReps} @intensity:{self.Intensity}, which means an INOL of:{self.INOL}"
    