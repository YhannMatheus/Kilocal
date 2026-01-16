from src.types.models.exercise import Exercisse
from src.types.schemas.exercise import *
from fastapi import HTTPException, status
from uuid import UUID

class ExerciseService:
    @staticmethod
    async def create(data: ExerciseCreate) -> Exercisse:
        try:
            exercise = await Exercisse.create(
                workout_id=data.workout_id,
                name=data.name,
                type=data.type,
                intensity=data.intensity
            )
            if not exercise:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create exercise"
                )
            return exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating exercise: {str(e)}"
            )
    
    @staticmethod
    async def get_by_id(exercise_id: UUID) -> Exercisse:
        exercise = await Exercisse.get_or_none(id=exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        return exercise
    
    @staticmethod
    async def update(exercise_id: UUID, data: ExerciseUpdate) -> Exercisse:
        exercise = await ExerciseService.get_by_id(exercise_id)
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(exercise, field, value)
        
        await exercise.save()
        return exercise
    
    @staticmethod
    async def delete(exercise_id: UUID) -> None:
        exercise = await ExerciseService.get_by_id(exercise_id)
        await exercise.delete()
