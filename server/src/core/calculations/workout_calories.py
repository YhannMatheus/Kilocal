from typing import Optional
from src.types.enums.exercise import IntensityLevelEnum
from src.types.enums.workout import TrainingTypeEnum

class WorkoutCalories:
    """
    Classe responsável pelos cálculos de gasto calórico usando Equivalentes Metabólicos (METs).
    """

    # Tabela de referência de METs
    MET_VALUES = {
        TrainingTypeEnum.CARDIO: {
            IntensityLevelEnum.LOW: 3.5,     # Caminhada leve
            IntensityLevelEnum.MODERATE: 5.0,# Trote / Caminhada rápida
            IntensityLevelEnum.HIGH: 8.0,    # Corrida
            IntensityLevelEnum.VERY_HIGH: 11.0, # Sprint / Corrida intensa
        },
        TrainingTypeEnum.STRENGTH: {
            IntensityLevelEnum.LOW: 3.0,     # Levantamento leve, muito descanso
            IntensityLevelEnum.MODERATE: 5.0,# Treino padrão de hipertrofia
            IntensityLevelEnum.HIGH: 6.0,    # Treino de força intenso / Powerlifting
            IntensityLevelEnum.VERY_HIGH: 8.0, # Circuitos com peso / CrossFit
        },
        TrainingTypeEnum.FLEXIBILITY: {
            IntensityLevelEnum.LOW: 2.0,     # Alongamento estático
            IntensityLevelEnum.MODERATE: 2.5,# Yoga leve
            IntensityLevelEnum.HIGH: 3.0,    # Pilates / Yoga intenso
            IntensityLevelEnum.VERY_HIGH: 4.0,
        },
        TrainingTypeEnum.SPORTS: {
            IntensityLevelEnum.LOW: 4.0,     # Vôlei recreativo, Tênis duplas
            IntensityLevelEnum.MODERATE: 6.0,# Tênis individual, Basquete treino
            IntensityLevelEnum.HIGH: 8.0,    # Futebol, Basquete jogo
            IntensityLevelEnum.VERY_HIGH: 10.0, # Artes marciais, Boxe
        },
        # Caso adicione Crossfit ou Funcional no enum futuramente
        TrainingTypeEnum.CROSSFIT: {
            IntensityLevelEnum.LOW: 5.0,
            IntensityLevelEnum.MODERATE: 8.0,
            IntensityLevelEnum.HIGH: 10.0,
            IntensityLevelEnum.VERY_HIGH: 12.0,
        }
    }

    @staticmethod
    def calculate_calories_from_met(
        met: float, weight_kg: float, duration_minutes: float
    ) -> float:
        """Fórmula base: Kcal = MET * Peso * Horas"""
        duration_hours = duration_minutes / 60
        calories = met * weight_kg * duration_hours
        return round(calories, 2)

    @staticmethod
    def calculate_single_set_calories(
        user_weight_kg: float,
        exercise_type: TrainingTypeEnum = TrainingTypeEnum.STRENGTH,
        reps: Optional[int] = None,
        weight_lifted_kg: Optional[float] = None,
        duration_seconds: Optional[float] = None,
        distance_meters: Optional[float] = None
    ) -> float:
        """
        Calcula as calorias gastas em um ÚNICO SET.
        Inteligente o suficiente para estimar duração se for treino de força (reps).
        """
        
        # 1. Determinar Duração Efetiva do Set
        estimated_duration_sec = 0
        
        if duration_seconds and duration_seconds > 0:
            estimated_duration_sec = duration_seconds
        elif reps and reps > 0:
            # Estimativa: Média de 4 segundos por repetição (fase concêntrica + excêntrica)
            # + uma pequena penalidade de descanso ativo se necessário
            estimated_duration_sec = reps * 4 
        else:
            # Se não tem tempo nem reps, não gera gasto calórico computável
            return 0.0

        duration_minutes = estimated_duration_sec / 60

        # 2. Determinar Intensidade Relativa
        intensity = IntensityLevelEnum.MODERATE
        
        if exercise_type == TrainingTypeEnum.STRENGTH and weight_lifted_kg is not None and user_weight_kg > 0:
             # Lógica: Intensidade baseada na carga relativa ao peso corporal
             ratio = weight_lifted_kg / user_weight_kg
             if ratio > 1.0: # Levantar mais que o próprio peso
                 intensity = IntensityLevelEnum.VERY_HIGH
             elif ratio > 0.7:
                 intensity = IntensityLevelEnum.HIGH
             elif ratio < 0.3: # Aquecimento ou leve
                 intensity = IntensityLevelEnum.LOW
        
        # TODO: Se fosse cardio, poderíamos usar velocidade (distance/time) para definir intensidade

        # 3. Buscar o valor MET correto
        met_table = WorkoutCalories.MET_VALUES.get(exercise_type, WorkoutCalories.MET_VALUES[TrainingTypeEnum.STRENGTH])
        met = met_table.get(intensity, 5.0)

        # 4. Calcular
        return WorkoutCalories.calculate_calories_from_met(
            met, user_weight_kg, duration_minutes
        )

    @staticmethod
    def calculate_workout_total_intensity(total_volume_kg: float, total_duration_min: float) -> str:
        """
        Retorna uma classificação de intensidade para o treino TODO baseada na densidade.
        (Volume Load / Tempo)
        """
        if total_duration_min <= 0:
            return IntensityLevelEnum.LOW.value
            
        density = total_volume_kg / total_duration_min
        
        if density > 800: return IntensityLevelEnum.VERY_HIGH.value
        if density > 500: return IntensityLevelEnum.HIGH.value
        if density > 300: return IntensityLevelEnum.MODERATE.value
        return IntensityLevelEnum.LOW.value