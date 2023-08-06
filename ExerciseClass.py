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




