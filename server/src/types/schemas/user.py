from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List
from uuid import UUID
from src.types.enums.user import GenderEnum
from src.types.schemas.workout import WorkoutRead
from src.types.schemas.body_assessment import BodyAssessmentGraphs

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    birth_date: date
    height_cm: Optional[float] = Field(None, gt=0, lt=300, description="Altura em cm") 
    gender: GenderEnum
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    userData: UserRead
    workouts: Optional[List[WorkoutRead]] = []
    body_graphs: Optional[BodyAssessmentGraphs] = None