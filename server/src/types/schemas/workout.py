from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from src.types.enums.workout import TrainingTypeEnum
from src.types.schemas.exercise import ExerciseRead, ExerciseMinimal

class WorkoutCreate(BaseModel):
    userid : UUID
    name: str = Field(..., min_length=1, max_length=255)
    type: TrainingTypeEnum
    start_time: datetime

class WorkoutRead(BaseModel):
    name: str
    type: TrainingTypeEnum
    start_time: datetime
    total_calories_burned: float = 0.0
    duration_minutes: Optional[float] = None
    exercises: List[ExerciseMinimal] = []
    class Config:
        from_attributes = True
class WorkoutDetailed(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    type: TrainingTypeEnum
    start_time: datetime
    end_time: Optional[datetime] = None
    total_calories_burned: float = 0.0
    duration_minutes: Optional[float] = None
    exercises: List[ExerciseRead] = []
    create_at: datetime

    class Config:
        from_attributes = True
        
class WorkoutCaloriesGraphPoint(BaseModel):
    date: datetime
    total_calories: float

class WorkoutDurationGraphPoint(BaseModel):
    date: datetime
    duration_minutes: float

class WorkoutPerformanceByTypeGraphPoint(BaseModel):
    date: datetime
    type: TrainingTypeEnum
    total_calories: float
    duration_minutes: float
    workouts_count: int = 1

class WorkoutGraphs(BaseModel):
    calories_graph: List[WorkoutCaloriesGraphPoint] = []
    duration_graph: List[WorkoutDurationGraphPoint] = []
    performance_by_type_graph: List[WorkoutPerformanceByTypeGraphPoint] = []

class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[TrainingTypeEnum] = None
    end_time: Optional[datetime] = None
