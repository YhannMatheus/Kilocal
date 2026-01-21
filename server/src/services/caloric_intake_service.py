from uuid import UUID
from datetime import date
from typing import Optional

from src.types.models.caloric_intakes import CaloricIntake
from src.types.schemas.caloric_intake import CaloricIntakeCreate, CaloricIntakeRead, DailyMacroSummary
from src.types.models.user import User

class CaloricIntakeService:
    @staticmethod
    def calculate_calories(protein: float, carbs: float, fats: float) -> float:
        """Calcula calorias baseadas nos macros (4-4-9)"""
        return (protein * 4) + (carbs * 4) + (fats * 9)

    @staticmethod
    async def add_meal(user_id: UUID, data: CaloricIntakeCreate) -> CaloricIntake:
        # Se as calorias não foram informadas, calcula automaticamente
        kcal = data.calories_consumed
        if kcal is None or kcal == 0:
            kcal = CaloricIntakeService.calculate_calories(
                data.protein_grams, 
                data.carbs_grams, 
                data.fats_grams
            )

        meal = await CaloricIntake.create(
            user_id=user_id,
            name=data.name,
            protein_grams=data.protein_grams,
            carbs_grams=data.carbs_grams,
            fats_grams=data.fats_grams,
            calories_consumed=kcal
        )
        return meal

    @staticmethod
    async def get_meals_by_date(user_id: UUID, query_date: date) -> list[CaloricIntake]:
        return await CaloricIntake.filter(
            user_id=user_id, 
            date=query_date
        ).order_by("created_at")

    @staticmethod
    async def get_daily_summary(user_id: UUID, query_date: date) -> DailyMacroSummary:
        meals = await CaloricIntakeService.get_meals_by_date(user_id, query_date)
        
        total_kcal = sum(m.calories_consumed for m in meals)
        total_prot = sum(m.protein_grams for m in meals)
        total_carbs = sum(m.carbs_grams for m in meals)
        total_fats = sum(m.fats_grams for m in meals)

        # Convertendo para schema de leitura
        meals_read = [CaloricIntakeRead.model_validate(m) for m in meals]

        return DailyMacroSummary(
            date=query_date,
            total_calories=round(total_kcal, 2),
            total_protein=round(total_prot, 2),
            total_carbs=round(total_carbs, 2),
            total_fats=round(total_fats, 2),
            entries=meals_read
        )
