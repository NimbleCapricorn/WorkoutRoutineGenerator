from Difficulty import *
from ExerciseClass import *
def createExerciseRow(name, VolumeSetting:Volume, IntensitySetting:Intensity):
    volume=VolumeSetting.value
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
        if  IntensityIterator.name == IntensitySetting:
            IntermittentIntensity=IntensityIterator
    Intensity=round(IntermittentIntensity.IntensityFunction(temporaryReps),1) 
    return name, volume, 3, Intensity