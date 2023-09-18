import numpy as np
from WeekClass import *

class IntensityFunction:
   name:Intensity
   IntensityFunction=np.poly((0,0,0,0))
   def __init__(self, name, amplitudes):
      self.name=name
      self.IntensityFunction=np.poly1d(amplitudes)
   def __str__(self):
      return f"The selected intensity is {self.name}" 
   
#Intensity functions to make generating varying intensity weeks easier
MaxIntensity=IntensityFunction("MAX", [-0.0405, 0.6583, -5.776, 104.87])
HeavyPIntensity=IntensityFunction("HEAVYP", [-0.0049, +0.1003, -3.411, 97.711])
HeavyIntensity=IntensityFunction("HEAVY", [-0.01, + 0.1733, -0.4844, 92.825])
ModPIntensity=IntensityFunction("MODP", [-0.0124, + 0.2095, - 0.2897, 82.753])
ModIntensity=IntensityFunction("MOD", [-0.0131, 0.2206, -0.1739, 77.707])
LightPIntensity=IntensityFunction("LIGHTP",[-0.0124, 0.2095, -0.2897, 82.753])
LightIntensity=IntensityFunction("LIGHT",[-0.0143, 0.2387, -0.0766, 72.67])

IntensityList=[MaxIntensity,HeavyPIntensity,HeavyIntensity,ModPIntensity,ModIntensity,LightPIntensity,LightIntensity]