from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional, List
from src.types.enums.workout import TrainingTypeEnum
from src.types.schemas.set import SetRead, SetCreate

# --- Schemas de Input ---

class WorkoutCreate(BaseModel):
    user_id: UUID4
    name: str = Field(..., min_length=1, max_length=255)
    type: TrainingTypeEnum
    start_time: datetime
    sets: List[SetCreate] = []

class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[TrainingTypeEnum] = None
    end_time: Optional[datetime] = None

# --- Schemas de Output ---

class WorkoutRead(BaseModel):
    id: UUID4
    name: str
    type: TrainingTypeEnum
    start_time: datetime
    total_calories_burned: float = 0.0
    duration_minutes: Optional[float] = None
    # Alterado de exercises -> sets
    sets: List[SetRead] = [] 
    
    class Config:
        from_attributes = True

class WorkoutDetailed(WorkoutRead):
    user_id: UUID4
    end_time: Optional[datetime] = None
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