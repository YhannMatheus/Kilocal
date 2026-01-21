from src.types.models.sets import Set
from src.types.models.workout import Workout
from src.types.models.exercise import Exercise
from src.types.schemas.set import SetCreate, SetUpdate
from src.core.calculations.workout_calories import WorkoutCalories
from src.types.enums.workout import TrainingTypeEnum 

# IMPORTANTE: Importar o modelo de avaliação corporal
from src.types.models.body_assessments import BodyAssessment 

from fastapi import HTTPException
from uuid import UUID

class SetService:

    @staticmethod
    async def get_user_current_weight(user_id: str) -> float:
        """
        Método auxiliar para buscar o peso mais recente do usuário.
        Se não houver histórico, retorna 70kg como fallback.
        """
        latest_assessment = await BodyAssessment.filter(user_id=user_id)\
                                                .order_by('-created_at')\
                                                .first()
        
        if latest_assessment and latest_assessment.weight_kg:
            return float(latest_assessment.weight_kg)
        
        return 70.0 # Peso padrão para cálculo se não houver registros

    @staticmethod
    async def add_set_to_workout(workout_id: UUID, data: SetCreate) -> Set:
        # Carregamentos básicos
        workout = await Workout.get_or_none(id=workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Treino não encontrado")
            
        exercise = await Exercise.get_or_none(id=data.exercise_id)
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercício não encontrado")

        # CORREÇÃO: Busca o peso na tabela de histórico
        # Como user_id no workout é UUID, converte para str se necessário pelo Tortoise
        # Usamos user_id direto para evitar fetch desnecessário
        user_weight = await SetService.get_user_current_weight(str(workout.user_id))
        
        # O tipo de treino vem do Workout (Strength, Cardio, etc)
        exercise_enum_value = workout.type

        cal_burned = WorkoutCalories.calculate_single_set_calories(
            user_weight_kg=user_weight,
            exercise_type=exercise_enum_value, 
            reps=data.reps,
            weight_lifted_kg=data.weight,
            duration_seconds=data.duration,
            distance_meters=data.distance
        )

        new_set = await Set.create(
            workout=workout,
            exercise=exercise,
            reps=data.reps,
            weight=data.weight,
            duration=data.duration,
            distance=data.distance,
            calories_burned=cal_burned
        )

        await SetService._update_workout_totals(workout)
        
        await new_set.fetch_related("exercise")
        return new_set

    @staticmethod
    async def update_set(set_id: UUID, data: SetUpdate) -> Set:
        # Prefetch workout para pegar o ID do user dele
        set_item = await Set.get_or_none(id=set_id).prefetch_related("workout", "exercise")
        if not set_item:
            raise HTTPException(status_code=404, detail="Set não encontrado")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(set_item, key, value)

        # CORREÇÃO: Busca peso mais recente do dono do treino
        user_weight = await SetService.get_user_current_weight(str(set_item.workout.user_id))
        
        # O tipo de treino vem do Workout
        exercise_enum_value = set_item.workout.type

        set_item.calories_burned = WorkoutCalories.calculate_single_set_calories(
            user_weight_kg=user_weight,
            exercise_type=exercise_enum_value,
            reps=set_item.reps,
            weight_lifted_kg=set_item.weight,
            duration_seconds=set_item.duration,
            distance_meters=set_item.distance
        )
        
        await set_item.save()
        await SetService._update_workout_totals(set_item.workout)
        
        return set_item

    # delete_set e _update_workout_totals mantêm-se iguais...
    @staticmethod
    async def delete_set(set_id: UUID) -> None:
        set_item = await Set.get_or_none(id=set_id).prefetch_related("workout")
        if not set_item:
            raise HTTPException(status_code=404, detail="Set not found")
        
        workout = set_item.workout
        await set_item.delete()
        await SetService._update_workout_totals(workout)

    @staticmethod
    async def _update_workout_totals(workout: Workout):
        sets = await Set.filter(workout=workout).all()
        workout.total_calories_burned = sum(s.calories_burned for s in sets)
        await workout.save()