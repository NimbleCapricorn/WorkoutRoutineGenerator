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

class INOL(Enum): 
    Deload=0.4             #under 0.4 is too little for stimulating growth, but is perfect for deloading while still practicing skills
    DailyRecoverable=1.0    #between 0.4 and 1.0 is recoverable stimulus (next day you can repeat the same workout basically)
    LoadAccumulating=2.0    #1.0 to 2.0 is accumulating fatigue, with bigger strength gains (only once you fully recover, though)
                            #above 2.0 lies madness

@dataclass
class INOL_Taget:
    name:str
    value:float

INOL_Targets=[INOL_Taget("Deload", 0.4), INOL_Taget("DailyRecoverable", 1.0), INOL_Taget("LoadAccumulating", 2.0)]