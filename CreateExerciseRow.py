from Difficulty import *
from ExerciseClass import *
def createExerciseRow(name, VolumeSetting:Volume, IntensitySetting:Intensity, INOL_Target:INOL_Target):
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
    if VolumeSetting.name == 'LOW':
        temporaryReps=temporaryExercise.maxRepetitions
    elif VolumeSetting.name == 'MED':
        temporaryReps=round((temporaryExercise.maxRepetitions+temporaryExercise.minRepetitions)/2)
    elif VolumeSetting.name == "HIGH":
        temporaryReps=temporaryExercise.minRepetitions
    elif temporaryReps > 40 | temporaryReps <= 0:
        print("repcount out of range")


    #calculate intensity based on determined repcount and given intensity setting
    for IntensityIterator in IntensityList:
        if  IntensityIterator.name == IntensitySetting.name:
            IntermittentIntensity=IntensityIterator
    Intensity=round(IntermittentIntensity.IntensityFunction(temporaryReps),1)

    INOL=(setcount*temporaryReps)/(100-Intensity) #Intensity Plus Number Of Lifts is a common number to self-check a program.

    #Depending on the INOL target setting, to achieve a good stimulus, set numbers may need to be bumped up or down as well
    while (abs(INOL-INOL_Target.value)/INOL_Target.value)>0.1:
        if (abs(INOL_Target.value-INOL)/INOL_Target.value>0.3 and INOL < INOL_Target.value):
            if VolumeSetting.name == 'LOW':
                setcount=3
            elif VolumeSetting.name == 'MED':
                setcount=4
            elif VolumeSetting.name == "HIGH":
                setcount=5
        elif(abs(INOL-INOL_Target.value)/INOL_Target.value>0.3 and INOL > INOL_Target.value):
            if VolumeSetting.name == 'LOW':
                setcount=2
            elif VolumeSetting.name == 'MED':
                setcount=2
            elif VolumeSetting.name == "HIGH":
                setcount=3
        INOL=(setcount*temporaryReps)/(100-Intensity)
        if (abs(INOL_Target.value-INOL)/INOL_Target.value>0.04 and INOL < INOL_Target.value ):
            Intensity+=1
        elif(abs(INOL-INOL_Target.value)/INOL_Target.value>0.04 and INOL > INOL_Target.value):
            Intensity-=1
        INOL=(setcount*temporaryReps)/(100-Intensity)

    
    return name, setcount, temporaryReps, Intensity, INOL