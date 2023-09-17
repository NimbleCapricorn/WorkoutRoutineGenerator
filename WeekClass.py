from dataclasses import dataclass
from typing import Literal
Volume=Literal["LOW","MED","HIGH"]
Intensity=Literal["LIGHT","LIGHTP","MOD","MODP","HEAVY","HEAVYP","MAX"]
@dataclass       
class Week:
    volume:Volume
    intensity:Intensity

