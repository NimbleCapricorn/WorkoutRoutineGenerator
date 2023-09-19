from Difficulty import *
from ExerciseClass import *
def createExerciseRow(name, VolumeSetting:Volume, IntensitySetting:Intensity):
    Name=name
    volume=VolumeSetting.value
    IntermittentIntensity:IntensityFunction
    for IntensityIterator in IntensityList:
        if  IntensityIterator.name == IntensitySetting:
            IntermittentIntensity=IntensityIterator
    Intensity=round(IntermittentIntensity.IntensityFunction(3),1) #how many reps you want to do
    return Name, volume, 3, Intensity