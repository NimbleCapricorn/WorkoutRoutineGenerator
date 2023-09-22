from ExerciseClass import *

class ProgramDay:
    Name:str
    ExerciseList:DailyExercise=[]
    pass

class ProgramWeek:
    ID=int
    ProgramDays:ProgramDay=[]
    pass

class ProgramMonth:
    ID=int
    ProgramWeeks:ProgramWeek=[]
    pass