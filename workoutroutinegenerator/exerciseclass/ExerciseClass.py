from dataclasses import *
from yaml import *
from workoutroutinegenerator.exerciseclass.difficulty import Difficulty
from workoutroutinegenerator.exerciseclass.difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOLTarget, INOLBorder, INOLBorders

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
    INOLValue:float

    def getINOLBorders(self, INOLTargetWithPriority):
                    if INOLTargetWithPriority.value <= INOLBorders[0].value:
                        return [0.0, 0.4]
                    if  INOLTargetWithPriority.value >=INOLBorders[0].value and  INOLTargetWithPriority.value <= INOLBorders[1].value:
                        return [0.4, 1.0]
                    else:
                        return [1.0, 2.0]
                    
                    
    def checkINOLisInRange(self, number, lower_bound, upper_bound):
        return lower_bound <= number <= upper_bound

    def calculateINOL(self, setcount, temporaryReps, Intensity):
        return (setcount*temporaryReps)/(100-Intensity)
    
    def calculateErrorFromINOL(self, INOL, INOL_Target):
        return ((INOL-INOL_Target.value)/INOL_Target.value)

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

    def __init__(self, weeknumber, day, CallingExercise, VolumeSetting:Volume, IntensitySetting:Intensity, INOL_Target:INOLTarget, DayINOLSetting:float):
        self.WeekIndex=weeknumber
        self.Day=day
        IntermittentIntensity:Difficulty.IntensityFunction
        self.NumberOfSets=VolumeSetting.value


        INOLTargetWithPriority=INOLBorder(INOL_Target.name, INOL_Target.value/(CallingExercise.Priority*DayINOLSetting)) #TODO#this is why the INOLBorder class is a stupid name

        INOLBorders=self.getINOLBorders(INOLTargetWithPriority)

        #determine best rep number for the volume setting
        match VolumeSetting.name: 
            case Volume.VLOW.name:
                self.NumberOfReps=CallingExercise.minRepetitions
            case Volume.LOW.name:
                self.NumberOfReps=round(CallingExercise.minRepetitions*1.3)
            case Volume.MED.name:
                self.NumberOfReps=round((CallingExercise.maxRepetitions+CallingExercise.minRepetitions)/2)
            case Volume.MEDP.name:
                self.NumberOfReps=round(CallingExercise.minRepetitions*1.3)
            case Volume.HIGH.name:
                self.NumberOfReps=round(CallingExercise.maxRepetitions/1.3)
            case Volume.VHIGH.name:
                self.NumberOfReps=CallingExercise.maxRepetitions



        #calculate intensity based on determined repcount and given intensity setting
        for IntensityIterator in Difficulty.IntensityList:
            if  IntensityIterator.name == IntensitySetting.name:
                IntermittentIntensity=IntensityIterator
        self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)

        self.INOLValue=self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity) #Intensity Plus Number Of Lifts is a common number to self-check a program.

        #calculate whether you are in the INOL target range 
        while not self.checkINOLisInRange(self.INOLValue, *INOLBorders):
            if self.calculateErrorFromINOL(self.INOLValue, INOLTargetWithPriority) < 0:
                if self.calculateErrorFromINOL(self.INOLValue, INOLTargetWithPriority)<-0.5:
                    self.NumberOfSets+=1
                if self.calculateErrorFromINOL(self.INOLValue, INOLTargetWithPriority)<-0.2:
                    FurtherChangesPossible=self.SetNumberOfReps(CallingExercise, self.NumberOfReps+1)
                    self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)
                    if not FurtherChangesPossible:
                        break
                else:
                    self.Intensity+=0.3
            else:
                if self.calculateErrorFromINOL(self.INOLValue, INOLTargetWithPriority)>0.5:
                    self.NumberOfSets-=1
                if self.calculateErrorFromINOL(self.INOLValue, INOLTargetWithPriority)>0.2:
                    FurtherChangesPossible=self.SetNumberOfReps(CallingExercise, self.NumberOfReps-1)
                    self.Intensity=round(IntermittentIntensity.IntensityFunction(self.NumberOfReps),1)
                    if not FurtherChangesPossible:
                        break
                else:
                    self.Intensity+=0.3
            self.INOLValue=self.calculateINOL(self.NumberOfSets,self.NumberOfReps,self.Intensity)

        
                    
        
        self.Intensity=round(self.Intensity,1)
        self.INOLValue=round(self.calculateINOL(self.NumberOfSets, self.NumberOfReps, self.Intensity),1)
        
        self.Name=CallingExercise.Name

    @classmethod
    def from_args(cls, weekindex:int, day:str, name:str, NumberOfSets:int, NumberOfReps:int, intensity:float, INOLTarget:float): 
        instance=cls(0, "Monday", Exercise("snatch", 1, 4, 1.0, False), Volume.LOW, Intensity.MOD, INOLTarget.DailyRecoverable, 1.0) #these parameters are gonna be overwritten, but can't create new instance  without some data
        instance.WeekIndex=weekindex
        instance.Day=day
        instance.Name=name
        instance.NumberOfSets=NumberOfSets
        instance.NumberOfReps=NumberOfReps
        instance.Intensity=intensity
        instance.INOLValue=INOLTarget
        return instance

    def __str__(self):
        return f"Exercise named:{self.Name}, number of sets:{self.NumberOfSets}, number of reps:{self.NumberOfReps} @intensity:{self.Intensity}, which means an INOL of:{self.INOLValue}"
    
@dataclass
class ProgramSettingDay:
    Name:str
    ExerciseList:str