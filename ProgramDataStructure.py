from ExerciseClass import *
from dataclasses import *
#from numpy import *

@dataclass
class ProgramDay:
    Name:str
    ExerciseList:DailyExercise

@dataclass
class ProgramWeek:
    ID:int
    ProgramDays:ProgramDay

@dataclass
class ProgramMonth:
    ID:int
    ProgramWeeks:ProgramWeek