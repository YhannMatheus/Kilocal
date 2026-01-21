from pydantic import BaseModel, UUID4
from typing import Optional
from src.types.enums.exercise import MuscleGroupEnum

class ExerciseBase(BaseModel):
    name: str
    target_muscle: MuscleGroupEnum

class ExerciseSimpleSchema(ExerciseBase):
    id: UUID4
    
    class Config:
        from_attributes = True

class ExerciseCreate(ExerciseBase):
    target_muscle: MuscleGroupEnum = MuscleGroupEnum.CHEST
    instructions: Optional[str] = None

class ExerciseResponseSchema(ExerciseCreate):
    id: UUID4
    is_system_default: bool
    is_custom: bool 

    class Config:
        from_attributes = True