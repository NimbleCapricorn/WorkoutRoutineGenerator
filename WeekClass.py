from dataclasses import dataclass
from typing import Literal
from enum import Enum
class Volume(Enum): #Make it configurable, how many sets volume settings mean
    LOW=2
    MED=3
    HIGH=4
Intensity=Literal["LIGHT","LIGHTP","MOD","MODP","HEAVY","HEAVYP","MAX"]
@dataclass       
class Week:
    volume:Volume
    intensity:Intensity

