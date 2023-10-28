from enum import Enum
from dataclasses import dataclass
class Volume(Enum):
    VLOW=1 
    LOW=2
    MED=3
    MEDP=4
    HIGH=5
    VHIGH=6

class Intensity(Enum):
    LIGHT=0
    LIGHTP=1
    MOD=2
    MODP=3
    HEAVY=4
    HEAVYP=5
    MAX=6

class INOLTarget(Enum): 
    Deload=0.4             #under 0.4 is too little for stimulating growth, but is perfect for deloading while still practicing skills
    DailyRecoverable=0.7    #between 0.4 and 1.0 is recoverable stimulus (next day you can repeat the same workout basically)
    LoadAccumulating=1.5    #1.0 to 2.0 is accumulating fatigue, with bigger strength gains (only once you fully recover, though)
                            #above 2.0 lies madness

@dataclass
class INOLBorder:
    name:str
    value:float

INOLBorders=[INOLBorder("Deload", 0.40), INOLBorder("DailyRecoverable", 1.0), INOLBorder("LoadAccumulating", 2.0)]