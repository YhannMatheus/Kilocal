"""Enums relacionados a usuários"""

from enum import Enum


class GenderEnum(str, Enum):
    """Gênero do usuário"""
    MALE = "male"
    FEMALE = "female"


class ActivityLevelEnum(str, Enum):
    """Nível de atividade física do usuário"""
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"
    ATHLETE = "athlete"


class RoleEnum(str, Enum):
    """Papel/permissão do usuário no sistema"""
    USER = "user"
    ADMIN = "admin"
