from dataclasses import *
@dataclass
class Exercise:
   name:str
   minRepetitions:int
   maxRepetitions:int 
   def __str__(self):
       return f"{self.name}"    
