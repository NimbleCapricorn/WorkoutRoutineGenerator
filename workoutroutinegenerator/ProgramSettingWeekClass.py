from dataclasses import dataclass
from .exerciseclass.difficulty.enumdefinitions.EnumDefinitions import Volume, Intensity, INOL, INOL_Targets


@dataclass       
class ProgramSettingWeek:
    Volume:Volume
    Intensity:Intensity
    INOL_Target:INOL

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
        case INOL.Deload.name:
            return INOL.Deload
        case INOL.DailyRecoverable.name:
            return INOL.DailyRecoverable
        case INOL.LoadAccumulating.name:
            return INOL.DailyRecoverable
    return "INOL_Target setting set in the config file not found"