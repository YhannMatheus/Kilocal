from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class CaloricIntakeBase(BaseModel):
    name: str = Field(..., description="Nome da refeição")
    protein_grams: float = Field(0.0, ge=0)
    carbs_grams: float = Field(0.0, ge=0)
    fats_grams: float = Field(0.0, ge=0)
    calories_consumed: Optional[float] = Field(None, ge=0, description="Se omitido, será calculado automaticamente")

class CaloricIntakeCreate(CaloricIntakeBase):
    pass

class CaloricIntakeRead(CaloricIntakeBase):
    id: UUID
    user_id: UUID
    date: date
    created_at: datetime
    
    # Assegura que calories_consumed nunca é None na leitura
    calories_consumed: float 

    class Config:
        from_attributes = True

class DailyMacroSummary(BaseModel):
    date: date
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    entries: list[CaloricIntakeRead]
