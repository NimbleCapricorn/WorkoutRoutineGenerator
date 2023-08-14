import ExerciseClass
class WorkoutDay:
    pass #TODO megcsinálni, hogy a workoutdayben egy darab array van, ami üres elsőre, és dailyExercise-okat tárol, valamint egy add operátor van rajta, ami hozzáad egy daily exercise-
    #ot az arrayhez
class Week:
    days=[]
    def __init__(self, numberOfDays, days):
        i=0
        for i in range(numberOfDays):
            self.days.append(WorkoutDay())


