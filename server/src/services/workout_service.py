from src.types.models.workout import Workout
from src.types.schemas.workout import *
from fastapi import HTTPException, status
from datetime import date

class WorkoutService:
    @staticmethod
    async def create_workout(data : WorkoutCreate) -> str:
        try:
            workout = await Workout.create(**data.dict())
            if not workout:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create workout"
                )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating workout: {str(e)}"
            )
        
        return str(workout.id)
    
    @staticmethod
    async def get_all_user_workouts(user_id: str) -> list[WorkoutRead]:
        try:
            workouts = await Workout.filter(user_id=user_id).prefetch_related("exercises").all()
            if not workouts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No workouts found for the user"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workouts: {str(e)}"
            )
        
        return [WorkoutRead(
            name=workout.name,
            type=workout.type,
            start_time=workout.start_time,
            total_calories_burned=workout.total_calories_burned,
            duration_minutes=workout.duration_minutes,
            exercises=[ExerciseMinimal.from_orm(ex) for ex in workout.exercises],
        ) for workout in workouts]
    
    @staticmethod
    async def get_workout_by_id(workout_id: str) -> WorkoutDetailed:
        try:
            workout = await Workout.get_or_none(id=workout_id)
            if workout is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout not found"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workout: {str(e)}"
            )
        
        return WorkoutDetailed(
                id=workout.id,
                user_id=workout.user.id,
                name=workout.name,
                type=workout.type,
                start_time=workout.start_time,
                end_time=workout.end_time,
                total_calories_burned=workout.total_calories_burned,
                duration_minutes=workout.duration_minutes,
                exercises=[ExerciseRead.from_orm(ex) for ex in workout.exercises],
                create_at=workout.create_at
            )
    
    @staticmethod
    async def update_workout(workout_id: str, data: WorkoutUpdate) -> None:
        try:
            workout = await Workout.get_or_none(id=workout_id)
            if workout is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout not found"
                )
            
            for field, value in data.dict(exclude_unset=True).items():
                setattr(workout, field, value)
            
            await workout.save()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating workout: {str(e)}"
            )
        
    @staticmethod
    async def delete_workout(workout_id: str) -> None:
        try:
            workout = await Workout.get_or_none(id=workout_id)
            if workout is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout not found"
                )
            
            await workout.delete()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting workout: {str(e)}"
            )
        
    @staticmethod
    async def get_all_workout_day(user_id: str) -> list[date]:
        try:
            workouts = await Workout.filter(user_id=user_id).all()
            if not workouts:
                return []
            
            workout_days = set()
            for workout in workouts:
                workout_days.add(workout.start_time.date())
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workout days: {str(e)}"
            )
        
        return sorted(list(workout_days))
    
    @staticmethod
    async def get_calories_by_all_days(user_id: str) -> list[tuple[date, float]]:
        try:
            workouts = await Workout.filter(user_id=user_id).all()
            
            if not workouts:
                return []
            
            calories_by_day: dict[date, float] = {}
            
            for workout in workouts:
                workout_date = workout.start_time.date()
                if workout_date in calories_by_day:
                    calories_by_day[workout_date] += workout.total_calories_burned
                else:
                    calories_by_day[workout_date] = workout.total_calories_burned
            
            result = sorted(calories_by_day.items(), key=lambda x: x[0])
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving calories by day: {str(e)}"
            )
        
        return result