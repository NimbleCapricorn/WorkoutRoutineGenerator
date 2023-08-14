import numpy as np
#the block below was supposed to support difficulties as raw data table.
# class Difficulty:
#    name=""
#    lowerLimit=0
#    upperLimit=10
#    def __init__(self, name, lowerLimit, upperLimit):
#       self.name=name
#       self.lowerLimit=lowerLimit
#       self.upperLimit=upperLimit
class IntensityFunction:
   name=""
   IntensityFunction=np.poly(0)
   def __init_(self, name, amplitudes):
      self.name=name
      self.IntensityFunction=np.poly(*amplitudes)
   def __str__(self):
      return f"The selected intensity is {self.name}" 