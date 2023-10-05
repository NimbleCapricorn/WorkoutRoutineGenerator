from dataclasses import *
import csv
from Difficulty import *
from ExerciseClass import *
from WeekClass import *

@dataclass
class Exercise:
   Name:str
   minRepetitions:int #minimum number or repetitions that can be prescribed in a set
   maxRepetitions:int #maximum number or repetitions that can be prescribed in a set
   Priority:float # float between 0.5 and 1 where 0.5 is the highest and 1 is the lowest. (0.5 means a 2x increase in INOL, so use sparingly)
   def __str__(self):
       return f"{self.Name}"    
   
#read exercises
ExerciseList:Exercise=[]
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = Exercise(str(row[0]), int(row[1]), int(row[2]), float(row[3]))
        ExerciseList.append(newExercise)

@dataclass
class DailyExercise:
    Name:str
    NumberOfSets:int
    NumberOfReps:int
    Intensity:float
    INOL:float

    def calculateINOL(self, setcount, temporaryReps, Intensity):
        return (setcount*temporaryReps)/(100-Intensity)
    
    def calculateErrorFromINOL(self, INOL, INOL_target):
        return ((INOL-INOL_target)/INOL_target)
    
    def __init__(self, name, VolumeSetting:Volume, IntensitySetting:Intensity, INOL_Target:INOL_Target):
        INOL:float=0.0
        setcount=VolumeSetting.value
        #temporary values to make calcuations easier
        temporaryReps:int
        temporaryExercise:Exercise
        IntermittentIntensity:IntensityFunction

        #find which exercise it is  ##TODO## what happens if we can't find the exercise?
        for ExerciseIterator in ExerciseList: 
            if ExerciseIterator.Name == name: 
                temporaryExercise=ExerciseIterator

        INOL_TargetWithPriority=INOL_Target.value/temporaryExercise.Priority

        #determine best rep number for the volume setting
        match VolumeSetting.name: 
            case Volume.LOW.name:
                temporaryReps=temporaryExercise.maxRepetitions
            case Volume.MED.name:
                temporaryReps=round((temporaryExercise.maxRepetitions+temporaryExercise.minRepetitions)/2)
            case Volume.HIGH.name:
                temporaryReps=temporaryExercise.minRepetitions



        #calculate intensity based on determined repcount and given intensity setting
        for IntensityIterator in IntensityList:
            if  IntensityIterator.name == IntensitySetting.name:
                IntermittentIntensity=IntensityIterator
        Intensity=round(IntermittentIntensity.IntensityFunction(temporaryReps),1)

        INOL=self.calculateINOL(setcount, temporaryReps, Intensity) #Intensity Plus Number Of Lifts is a common number to self-check a program.

        #Depending on the INOL target setting, to achieve a good stimulus, set numbers may need to be bumped up or down as well
        while (abs(self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)) > 0.20):
            #Very big error: correct set count
            if (self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)<-0.25):
                match VolumeSetting.name:
                    case Volume.LOW.name:
                        setcount=4
                    case Volume.MED.name:
                        setcount=5
                    case Volume.HIGH.name:
                        setcount=6
            elif(self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)>0.25):
                match VolumeSetting.name:
                    case Volume.LOW.name:
                        setcount=2
                    case Volume.MED.name:
                        setcount=3
                    case Volume.HIGH.name:
                        setcount=4
            INOL=self.calculateINOL(setcount, temporaryReps, Intensity)

            #semi-big error: change rep number
            if (self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)<-0.1 ):
                temporaryReps+=1
                Intensity=round(IntermittentIntensity.IntensityFunction(temporaryReps),1)
            elif(self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)>0.1 ):
                temporaryReps-=1
                Intensity=round(IntermittentIntensity.IntensityFunction(temporaryReps),1)
            INOL=self.calculateINOL(setcount, temporaryReps, Intensity)

            #small error:change intensity
            if (self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority)< - 0.05 ):
                Intensity+=0.3
            elif(self.calculateErrorFromINOL(INOL, INOL_TargetWithPriority) > 0.05 ):
                Intensity-=0.3
            INOL=self.calculateINOL(setcount, temporaryReps, Intensity)
        
        Intensity=round(Intensity,1)
        INOL=round(self.calculateINOL(setcount, temporaryReps, Intensity),1)
        
        self.Name=name
        self.NumberOfSets=setcount
        self.NumberOfReps=temporaryReps
        self.Intensity=Intensity
        self.INOL=INOL

    def __str__(self):
        return f"Exercise named:{self.Name}, number of sets:{self.NumberOfSets}, number of reps:{self.NumberOfReps} @intensity:{self.Intensity}, which means an INOL of:{self.INOL}"
    
