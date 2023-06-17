class Exercise:
    
    #Tempo and Variation aren't inherent to the exercise, those should be used only when generating the routine
    def __init__(self, MaxWeight, Bodyparts, OptimalLoadPercentage, isTechniqueFocused):
        self.MaxWeight = MaxWeight
        self.Bodyparts = Bodyparts
        self.OptimalLoadPercentage = OptimalLoadPercentage
        self.isTechniqueFocused = isTechniqueFocused

    def getisTechniqueFocused(self):
        return self.isTechniqueFocused

    def getOptimalLoadingPercentage(self):
        return self.OptimalLoadPercentage

    def getBodyparts(self):
        return self.Bodyparts

    def getMaxWeight(self):
        return self.MaxWeight
    
    pass




