class Progression:
    #MethofOfProgression can be linear, weekly undulating, daily undulating. TODO: later exland with Maxout, RPEBased progression methods
    #Contraints can be tonnage, OptimalLoadingPercentage, not yet used
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

    #Constrains are not used in this moment in time, but for expanded functionality it will be needed
    def getConstraints(self):
        return self.Contstraints

    pass


