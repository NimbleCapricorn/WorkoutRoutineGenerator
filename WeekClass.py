from dataclasses import dataclass
from enum import Enum
from random import *

class Volume(Enum):
    LOW=3
    MED=4
    HIGH=5

class Intensity(Enum):
    LIGHT=0
    LIGHTP=1
    MOD=2
    MODP=3
    HEAVY=4
    HEAVYP=5
    MAX=6

class INOL_Target(Enum): 
    Deload=0.3             #under 0.4 is too little for stimulating growth, but is perfect for deloading while still practicing skills
    DailyRecoverable=0.7    #between 0.4 and 1.0 is recoverable stimulus (next day you can repeat the same workout basically)
    LoadAccumulating=1.4    #1.0 to 2.0 is accumulating fatigue, with bigger strength gains (only once you fully recover, though)
                            #above 2.0 lies madness
@dataclass       
class Week:
    Volume:Volume
    Intensity:Intensity
    INOL_Target:INOL_Target

def searchVolumeSetting(setting:str):
    match setting:
        case Volume.LOW.name:
            return Volume.LOW
        case Volume.MED.name:
            return Volume.MED
        case Volume.HIGH.name:
            return Volume.HIGH
    return "volume setting set in the config file not found"

def searchIntensitySetting(setting:str):
    match setting:
        case Intensity.LIGHT.name:
            return Intensity.LIGHT
        case Intensity.LIGHTP.name:
            return Intensity.LIGHTP
        case Intensity.MOD.name:
            return Intensity.MOD
        case Intensity.MODP.name:
            return Intensity.MODP
        case Intensity.HEAVY.name:
            return Intensity.HEAVY
        case Intensity.HEAVYP.name:
            return Intensity.HEAVYP
        case Intensity.MAX.name:
            return Intensity.MAX

def searchINOLSetting(setting:str):
    match setting:
        case INOL_Target.Deload.name:
            return INOL_Target.Deload
        case INOL_Target.DailyRecoverable.name:
            return INOL_Target.DailyRecoverable
        case INOL_Target.LoadAccumulating.name:
            return INOL_Target.DailyRecoverable