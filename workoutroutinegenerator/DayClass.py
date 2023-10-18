from dataclasses import dataclass
from yaml import *

@dataclass
class DayClass:
    name:str
    DayINOLPriority:float

with open('Days.yml', 'r') as file:
    ProgramConfig = safe_load(file)
    DaySettingList=[]
    for DayConfigItem in ProgramConfig['Weekdays']:
        DaySettingList.append(DayClass(DayConfigItem['Name'], DayConfigItem['INOL_Priority']))