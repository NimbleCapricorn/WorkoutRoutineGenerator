class Exercise:
    
    def __init__(self, name, minRepetitions, maxRepetitions):
        self.name=name
        self.minRepetitions=minRepetitions
        self.maxRepetitions=maxRepetitions
    def __str__(self):
        return f"{1}".format(self.name)
    def getName(self):
        return self.name
    def getminRepetitions(self):
        return self.minRepetitions
    def getmaxRepetitions(self):
        return self.maxRepetitions
    
    pass

class DailyExercise(Exercise):
    
    def __init__(self, name, minRepetitions, maxRepetitions, percentageOfOneRepMax, Sets, Reps):
        Exercise.__init__(name, minRepetitions,maxRepetitions)
        self.percentageOfOneRepMax=percentageOfOneRepMax
        self.Sets=Sets
        self.Reps=Reps
    def getName(self):
        return self.name
    def getminRepetitions(self):
        return self.minRepetitions
    def getmaxRepetitions(self):
        return self.maxRepetitions
    def getpercentageOfOneRepMax(self):
        return self.percentageOfOneRepMax
    def getSets(self):
        return self.Sets
    def getReps(self):
        return self.Reps
    pass


