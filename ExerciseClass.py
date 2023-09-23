from dataclasses import *
import csv
from Difficulty import *
from ExerciseClass import *
from WeekClass import *

@dataclass
class Exercise:
   Name:str
   minRepetitions:int
   maxRepetitions:int 
   def __str__(self):
       return f"{self.Name}"    
   
#read exercises
ExerciseList:Exercise=[]
with open("Exercises.csv", "r") as ExercisesFile:
    reader = csv.reader(ExercisesFile, delimiter=";")
    
    for row in reader:
        newExercise = Exercise(str(row[0]), int(row[1]), int(row[2]))
        ExerciseList.append(newExercise)
   
class DailyExercise:
    Name:str
    NumberOfSets:int
    NumberOfReps:int
    Intensity:float
    INOL:float
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

        INOL=(setcount*temporaryReps)/(100-Intensity) #Intensity Plus Number Of Lifts is a common number to self-check a program.

        #Depending on the INOL target setting, to achieve a good stimulus, set numbers may need to be bumped up or down as well
        while (abs(INOL-INOL_Target.value)/INOL_Target.value) > 0.35 or (abs(INOL_Target.value-INOL)/INOL_Target.value) > 0.35:
            if ((INOL_Target.value-INOL)/INOL_Target.value>0.25):
                match VolumeSetting.name:
                    case Volume.LOW.name:
                        setcount=4
                    case Volume.MED.name:
                        setcount=5
                    case Volume.HIGH.name:
                        setcount=6
            elif((INOL-INOL_Target.value)/INOL_Target.value>0.25):
                match VolumeSetting.name:
                    case Volume.LOW.name:
                        setcount=2
                    case Volume.MED.name:
                        setcount=3
                    case Volume.HIGH.name:
                        setcount=4
            INOL=(setcount*temporaryReps)/(100-Intensity)
            if ((INOL_Target.value-INOL)/INOL_Target.value>0.01 ):
                Intensity+=0.3
            elif((INOL-INOL_Target.value)/INOL_Target.value>0.01 ):
                Intensity-=0.3
            INOL=(setcount*temporaryReps)/(100-Intensity)
        Intensity=round(Intensity,1)
        INOL=round((setcount*temporaryReps)/(100-Intensity),1)
        
        self.Name=name
        self.NumberOfSets=setcount
        self.NumberOfReps=temporaryReps
        self.Intensity=Intensity
        self.INOL=INOL

    def __str__(self):
        return f"Exercise named:{self.Name}, number of sets:{self.NumberOfSets}, number of reps:{self.NumberOfReps} @intensity:{self.Intensity}, which means an INOL of:{self.INOL}"
    
