from tortoise.expressions import Q
from src.types.models.exercise import Exercise
from src.types.schemas.exercise import ExerciseCreate
from src.types.models.user import User

class ExerciseService:
    @staticmethod
    async def get_all_available_exercises(user_id: str):
        return await Exercise.filter(
            Q(is_system_default=True) | Q(created_by_id=user_id)
        ).all()

    @staticmethod
    async def create_custom_exercise(user_id: str, data: ExerciseCreate):
        existing = await Exercise.filter(name=data.name, created_by_id=user_id).first()
        if existing:
            raise ValueError("Exercise name already exists")

        user = await User.get(id=user_id)
        return await Exercise.create(
            **data.model_dump(),
            is_system_default=False,
            created_by=user
        )
    @staticmethod
    async def delete_custom_exercise(user_id: str, exercise_id: str):
        exercise = await Exercise.get_or_none(id=exercise_id, created_by_id=user_id, is_system_default=False)
        if not exercise:
            raise ValueError("Exercise not found or cannot be deleted")

        await exercise.delete()