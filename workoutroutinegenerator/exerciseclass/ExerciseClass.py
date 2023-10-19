from dataclasses import *
from yaml import *
from .difficulty import Difficulty, enumdefinitions
from .difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOL_Target

@dataclass
class Exercise:
   Name:str
   minRepetitions:int #minimum number or repetitions that can be prescribed in a set
   maxRepetitions:int #maximum number or repetitions that can be prescribed in a set
   Priority:float # float between 0.5 and 1 where 0.5 is the highest and 1 is the lowest. (0.5 means a 2x increase in INOL, so use sparingly)
   generateWarmup:bool
   def __str__(self):
       return f"{self.Name}"    


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

    def __init__(self, weeknumber, day, CallingExercise, VolumeSetting:Volume, IntensitySetting:Intensity, INOL_Target:INOL_Target, DayINOLSetting:float):
        #temporary values to make calcuations easier
        self.WeekIndex=weeknumber
        self.Day=day
        IntermittentIntensity:Difficulty.IntensityFunction
        self.NumberOfSets=VolumeSetting.value


        INOL_TargetWithPriority=INOL_Target.value/(CallingExercise.Priority*DayINOLSetting)

        #determine best rep number for the volume setting
        match VolumeSetting.name: 
            case Volume.LOW.name:
                self.NumberOfReps=CallingExercise.maxRepetitions
            case Volume.MED.name:
                self.NumberOfReps=round((CallingExercise.maxRepetitions+CallingExercise.minRepetitions)/2)
            case Volume.HIGH.name:
                self.NumberOfReps=CallingExercise.minRepetitions



        #calculate intensity based on determined repcount and given intensity setting
        for IntensityIterator in Difficulty.IntensityList:
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
                    FurtherChangesPossible=self.SetNumberOfReps(CallingExercise, self.NumberOfReps+2)
                else:
                    FurtherChangesPossible=self.SetNumberOfReps(CallingExercise, self.NumberOfReps+1)
                self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)
                if not FurtherChangesPossible:
                    break
            while (self.calculateErrorFromINOL(self.INOL, INOL_TargetWithPriority) > (0.2/iterator) ):
                FurtherChangesPossible=self.SetNumberOfReps(CallingExercise, self.NumberOfReps-1)
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
        
        self.Name=CallingExercise.Name

    @classmethod
    def from_args(cls, weekindex:int, day:str, name:str, NumberOfSets:int, NumberOfReps:int, intensity:float, INOL:float): 
        instance=cls(0, "Monday", Exercise("snatch", 1, 4, 1.0, False), Volume.LOW, Intensity.MOD, INOL_Target.DailyRecoverable, 1.0) #these parameters are gonna be overwritten, but can't create new instance  without some data
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
    
@dataclass
class ProgramSettingDay:
    Name:str
    ExerciseList:str