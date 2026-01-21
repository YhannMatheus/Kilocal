"""Enums relacionados a treinos"""

from enum import Enum


class TrainingTypeEnum(str, Enum):
    """Estilo/Objetivo do Treino - Define o cálculo metabólico"""
    STRENGTH = "strength"      # Musculação tradicional
    CARDIO = "cardio"          # Corrida, Bike
    CROSSFIT = "crossfit"      # Alta intensidade mista
    FLEXIBILITY = "flexibility"# Yoga, Pilates
    SPORTS = "sports"          # Futebol, Vôlei
    BALANCE = "balance"
