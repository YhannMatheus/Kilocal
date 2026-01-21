from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import date, datetime
from typing import Optional

from src.services.caloric_intake_service import CaloricIntakeService
from src.types.schemas.caloric_intake import CaloricIntakeCreate, CaloricIntakeRead, DailyMacroSummary

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

@router.post("/meal", response_model=CaloricIntakeRead)
async def add_meal(data: CaloricIntakeCreate, request: Request):
    """Registra uma refeição"""
    user = request.state.user
    try:
        meal = await CaloricIntakeService.add_meal(user.id, data)
        return meal
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar refeição: {str(e)}"
        )

@router.get("/summary/{query_date}", response_model=DailyMacroSummary)
async def get_daily_summary(query_date: date, request: Request):
    """Retorna o resumo de macros e calorias de um dia específico"""
    user = request.state.user
    try:
        summary = await CaloricIntakeService.get_daily_summary(user.id, query_date)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar resumo nutricional: {str(e)}"
        )

@router.get("/summary/today", response_model=DailyMacroSummary)
async def get_today_summary(request: Request):
    """Atalho para pegar o resumo de hoje"""
    user = request.state.user
    today = datetime.now().date()
    try:
        summary = await CaloricIntakeService.get_daily_summary(user.id, today)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar resumo de hoje: {str(e)}"
        )
