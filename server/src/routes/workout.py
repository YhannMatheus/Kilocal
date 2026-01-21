from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from uuid import UUID

# Services
from src.services.workout_service import WorkoutService
from src.services.set_services import SetService

# Schemas
from src.types.schemas.workout import (
    WorkoutCreate, 
    WorkoutRead, 
    WorkoutUpdate, 
    WorkoutDetailed, 
    WorkoutGraphs
)
from src.types.schemas.set import (
    SetCreate, 
    SetRead, 
    SetUpdate
)

router = APIRouter(prefix="/workouts", tags=["Workouts"])

# --- DEPENDÊNCIA AUXILIAR ---
def get_user_id(request: Request) -> str:
    """
    Recupera o ID do usuário injetado pelo AuthMiddleware.
    O Middleware já garantiu que o token é válido e o usuário existe.
    """
    if not hasattr(request.state, "user_id"):
        # Segurança extra caso o middleware falhe ou a rota seja pública
        raise HTTPException(status_code=401, detail="User context missing")
    return str(request.state.user_id)

# ==========================================
#  ROTAS DE SETS (O Coração do Treino)
# ==========================================

@router.post("/{workout_id}/sets", response_model=SetRead, status_code=status.HTTP_201_CREATED)
async def add_set_to_workout(
    workout_id: UUID, 
    set_data: SetCreate,
    user_id: str = Depends(get_user_id) # <--- Usa a dependência leve do middleware
):
    """
    Adiciona um exercício (set) ao treino.
    Calcula calorias automaticamente (baseado no tipo de treino + peso do usuário).
    """
    return await SetService.add_set_to_workout(workout_id, set_data)

@router.put("/sets/{set_id}", response_model=SetRead)
async def update_set(
    set_id: UUID, 
    set_data: SetUpdate,
    user_id: str = Depends(get_user_id)
):
    """
    Atualiza um set existente (carga, reps, tempo).
    Recalcula automaticamente as calorias desse set e do treino todo.
    """
    return await SetService.update_set(set_id, set_data)

@router.delete("/sets/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_set(
    set_id: UUID,
    user_id: str = Depends(get_user_id)
):
    """Remove um set e desconta suas calorias do total."""
    await SetService.delete_set(set_id)
    return None

# ==========================================
#  ROTAS DE WORKOUT (Gerenciamento)
# ==========================================

@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout: WorkoutCreate, 
    user_id: str = Depends(get_user_id)
):
    """Inicia um novo treino (Header). Retorna o ID do treino criado."""
    # Validação extra: O ID no payload deve bater com o token
    if str(workout.user_id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create workout for another user")
    
    return await WorkoutService.create_workout(workout)

@router.get("/", response_model=List[WorkoutRead])
async def get_my_workouts(
    user_id: str = Depends(get_user_id)
):
    """Lista o histórico resumido de treinos do usuário logado."""
    return await WorkoutService.get_all_user_workouts(user_id)

@router.get("/{workout_id}", response_model=WorkoutDetailed)
async def get_workout_details(
    workout_id: str, 
    user_id: str = Depends(get_user_id)
):
    """
    Retorna o treino completo:
    - Dados gerais (Nome, Tipo, Calorias Totais)
    - Lista de todos os Sets realizados
    """
    return await WorkoutService.get_workout_by_id(workout_id)

@router.put("/{workout_id}")
async def update_workout_header(
    workout_id: str, 
    data: WorkoutUpdate, 
    user_id: str = Depends(get_user_id)
):
    """
    Usado para:
    1. Finalizar treino (enviar 'end_time')
    2. Mudar nome ou tipo do treino
    """
    await WorkoutService.update_workout(workout_id, data)
    return {"message": "Workout updated successfully"}

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: str, 
    user_id: str = Depends(get_user_id)
):
    """Apaga o treino e todos os seus sets."""
    await WorkoutService.delete_workout(workout_id)
    return None

# ==========================================
#  ROTAS DE GRÁFICOS (Dashboard)
# ==========================================

@router.get("/graphs/stats", response_model=WorkoutGraphs)
async def get_workout_stats(
    user_id: str = Depends(get_user_id)
):
    """
    Retorna dados agregados para os gráficos:
    - Calorias vs Tempo
    - Duração dos treinos
    - Performance por TIPO de treino
    """
    return await WorkoutService.get_graphs_data(user_id)