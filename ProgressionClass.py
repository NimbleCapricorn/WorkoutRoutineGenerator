from dataclasses import *
from enum import Enum
@dataclass
class ProgressionMethod(Enum):
    Linear=1
    DailyUndulating=2
    WeeklyUndulating=3

@dataclass
class Progression:
    Name:str
    MethodOfProgression:ProgressionMethod
    #Contstraints
     #Constrains are not used in this moment in time, but for expanded functionality it will be needed
    #TODO: later exland with Maxout, RPEBased progression methods
    #Contraints can be tonnage, OptimalLoadingPercentage, not yet used
    def __str__(self):
        return f"The Progression you selected is: {self.Name}"


