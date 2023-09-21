from dataclasses import dataclass
from enum import Enum
class Volume(Enum): ##TODO## Make it configurable, how many sets volume settings mean
    LOW=2
    MED=3
    HIGH=4

class Intensity(Enum):
    LIGHT=0
    LIGHTP=1
    MOD=2
    MODP=3
    HEAVY=4
    HEAVYP=5
    MAX=6

class INOL_Target(Enum): #TODO# this should be configurable as well [but these are scientific limits, so they should not be too far off for anyone]
    Deload=0.4              #under 0.4 is too little for stimulating growth, but is perfect for deloading while still practicing skills
    DailyRecoverable=1.0    #between 0.4 and 1.0 is recoverable stimulus (next day you can repeat the same workout basically)
    LoadAccumulating=2.0    #1.0 to 2.0 is accumulating fatigue, with bigger strength gains (only once you fully recover, though)
                            #above 2.0 lies madness
@dataclass       
class Week:
    volume:Volume
    intensity:Intensity
    INOL_Target:INOL_Target
