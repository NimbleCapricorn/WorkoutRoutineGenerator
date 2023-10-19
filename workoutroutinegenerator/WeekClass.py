from dataclasses import dataclass
from .exerciseclass.difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOL_Target


@dataclass       
class WeekSetting:
    Volume:Volume
    Intensity:Intensity
    INOL_Target:INOL_Target

def searchVolumeSetting(setting:str):
    match setting:
        case Volume.LOW.name:
            return Volume.LOW
        case Volume.MED.name:
            return Volume.MED
        case Volume.HIGH.name:
            return Volume.HIGH
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
        case INOL_Target.Deload.name:
            return INOL_Target.Deload
        case INOL_Target.DailyRecoverable.name:
            return INOL_Target.DailyRecoverable
        case INOL_Target.LoadAccumulating.name:
            return INOL_Target.DailyRecoverable
    return "INOL_Target setting set in the config file not found"