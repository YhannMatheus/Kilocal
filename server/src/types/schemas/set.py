from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional
from src.types.schemas.exercise import ExerciseSimpleSchema

class SetCreate(BaseModel):
    exercise_id: UUID4
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=0)
    distance: Optional[float] = Field(None, ge=0)

class SetUpdate(BaseModel):
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=0)

class SetRead(BaseModel):
    id: UUID4
    exercise: ExerciseSimpleSchema 
    reps: Optional[int]
    weight: Optional[float]
    duration: Optional[int]
    distance: Optional[float]
    calories_burned: float
    created_at: datetime

    class Config:
        from_attributes = True