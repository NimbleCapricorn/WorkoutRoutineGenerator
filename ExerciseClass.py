class Exercise:
    
    def __init__(self, Name, MaxWeight, Bodyparts, OptimalLoadPercentage, isTechniqueFocused):
        self.Name=Name
        self.MaxWeight = MaxWeight
        self.Bodyparts = Bodyparts
        self.OptimalLoadPercentage = OptimalLoadPercentage
        self.isTechniqueFocused = isTechniqueFocused
    def __str__(self):
        return "The exercise you selected is: "+self.Name+", with a max weight of: "+self.MaxWeight+" kg"
    def getName(self):
        return self.Name

    def getisTechniqueFocused(self):
        return self.isTechniqueFocused

    def getOptimalLoadingPercentage(self):
        return self.OptimalLoadPercentage

    def getBodyparts(self):
        return self.Bodyparts

    def getMaxWeight(self):
        return self.MaxWeight
    
    pass




