"""Enums relacionados a exercícios"""

from enum import Enum

class TrainingTypeEnum(str, Enum):
    """Intenção principal do exercício"""
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    SPORTS = "sports"
    CROSSFIT = "crossfit"

class MuscleGroupEnum(str, Enum):
    """Tipo de exercício por grupo muscular ou categoria"""
    BACK = "back"
    CHEST = "chest"
    LEGS = "legs"
    ARMS = "arms"
    SHOULDERS = "shoulders"
    ABDOMEN = "abdomen"
    CARDIO = "cardio"

class IntensityLevelEnum(str, Enum):
    """Nível de intensidade do exercício"""
    LOW = "low"
    MODERATE = "moderate"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
