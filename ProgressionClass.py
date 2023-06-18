class Progression:
    #MethofOfProgression can be linear, weekly undulating, daily undulating
    #Contraints can be tonnage, OptimalLoadingPercentage
    def __init__(self, Name, MethodOfProgression, Constraints):
        self.Name=Name
        self.MethodOfProgression = MethodOfProgression
        self.Contstraints = Constraints
    def __str__(self):
        return "The Progression you selected is: "+self.Name
    def getName(self):
        return self.Name

    def getMethodOfProgression(self):
        return self.MethodOfProgression

    def getConstraints(self):
        return self.Contstraints

    pass


