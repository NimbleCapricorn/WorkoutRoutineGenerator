class Exercise(MaxWeight, isNeurologicallyTaxing, isWholeBody , Bodyparts, OptimalLoadPercentage, isTechniqueFocused):
    
    #Tempo and Variation aren't inherent to the exercise, those should be used only when generating the routine
    MaxWeight = MaxWeight
    isNeurologicallyTaxing = isNeurologicallyTaxing
    isWholeBody = isWholeBody
    Bodyparts = Bodyparts
    OptimalLoadPercentage = OptimalLoadPercentage
    isTechniqueFocused = isTechniqueFocused

    def isTechniqueFocused(self):
        return self.isTechniqueFocused

    def OptimalLoadingPercentage(self):
        return self.OptimalLoadPercentage

    def Bodyparts(self):
        return self.Bodyparts

    def isWholeBody(self):
        return self.isWholeBody

    def isNeurologicallyTaxing(self):
        return self.isNeurologicallyTaxing

    def MaxWeight(self):
        return self.MaxWeight
    
    pass




