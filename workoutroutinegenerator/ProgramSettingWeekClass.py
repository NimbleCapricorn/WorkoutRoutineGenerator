from dataclasses import dataclass
from .exerciseclass.difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOLTarget, INOLBorders


@dataclass       
class ProgramSettingWeek:
    Volume:Volume
    Intensity:Intensity
    INOL_Target:INOLTarget

def searchVolumeSetting(setting:str):
    match setting:
        case Volume.VLOW.name:
            return Volume.VLOW
        case Volume.LOW.name:
            return Volume.LOW
        case Volume.MED.name:
            return Volume.MED
        case Volume.MEDP.name:
            return Volume.MEDP
        case Volume.HIGH.name:
            return Volume.HIGH
        case Volume.VHIGH.name:
            return Volume.VHIGH
    return "volume setting set in the config file not found"

def searchIntensitySetting(setting:str):
    match setting:
        case Intensity.LIGHT.name:
            return Intensity.LIGHT
        case Intensity.LIGHTP.name:
            return Intensity.LIGHTP
        case Intensity.MOD.name:
            return Intensity.MOD
        case Intensity.MODP.name:
            return Intensity.MODP
        case Intensity.HEAVY.name:
            return Intensity.HEAVY
        case Intensity.HEAVYP.name:
            return Intensity.HEAVYP
        case Intensity.MAX.name:
            return Intensity.MAX
    return "Intensity setting set in the config file not found"

def searchINOLSetting(setting:str):
    match setting:
        case INOLTarget.Deload.name:
            return INOLTarget.Deload
        case INOLTarget.DailyRecoverable.name:
            return INOLTarget.DailyRecoverable
        case INOLTarget.LoadAccumulating.name:
            return INOLTarget.DailyRecoverable
    return "INOLTarget setting set in the config file not found"