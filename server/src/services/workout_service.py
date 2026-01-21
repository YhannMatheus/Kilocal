from src.types.models.workout import Workout
from src.types.models.sets import Set
from src.types.schemas.workout import *
from fastapi import HTTPException, status
from datetime import date
from tortoise.transactions import in_transaction
from src.types.models.workout import Workout
from datetime import datetime
from src.types.models.workout import Workout
from src.types.schemas.workout import (
    WorkoutCreate, 
    WorkoutRead, 
    WorkoutUpdate, 
    WorkoutDetailed,
    # Importar schemas de gráficos
    WorkoutGraphs,
    WorkoutCaloriesGraphPoint,
    WorkoutDurationGraphPoint,
    WorkoutPerformanceByTypeGraphPoint
)

class WorkoutService:
    @staticmethod
    async def create_workout(data: WorkoutCreate) -> str:
        async with in_transaction() as conn:
            try:
                # 1. Criar o Workout principal
                workout_data = data.model_dump(exclude={'sets'})
                # O model_dump do pydantic v2 prefere essa nomenclatura. Se usar v1 é .dict()
                # Garanta que data.sets não vá para o Workout.create
                
                workout = await Workout.create(**workout_data, using_db=conn)
                
                # 2. Se houver sets no payload, cria-los agora
                if data.sets:
                    for set_item in data.sets:
                        await Set.create(
                            workout=workout,
                            exercise_id=set_item.exercise_id, 
                            reps=set_item.reps,
                            weight=set_item.weight,
                            duration=set_item.duration,
                            distance=set_item.distance,
                            using_db=conn
                        )
                
                return str(workout.id)
                
            except Exception as e:
                # O in_transaction fará rollback automático se der erro
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error creating workout with sets: {str(e)}"
                )
    
    @staticmethod
    async def get_all_user_workouts(user_id: str) -> list[WorkoutRead]:
        try:
            # Prefetch correto: sets -> exercise
            workouts = await Workout.filter(user_id=user_id)\
                .prefetch_related("sets__exercise")\
                .all()
            
            # O Pydantic (from_attributes=True) deve lidar com a conversão aninhada
            return [WorkoutRead.model_validate(w) for w in workouts]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workouts: {str(e)}"
            )
    
    @staticmethod
    async def get_workout_by_id(workout_id: str) -> WorkoutDetailed:
        try:
            workout = await Workout.get_or_none(id=workout_id)\
                .prefetch_related("sets__exercise")
            
            if workout is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout not found"
                )
            
            return WorkoutDetailed.model_validate(workout)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving workout: {str(e)}"
            )
    
    # ... Métodos update, delete e graphs permanecem similares, 
    # mas atualize update para não quebrar se sets não forem tratados aqui ...
    
    @staticmethod
    async def update_workout(workout_id: str, data: WorkoutUpdate) -> None:
        try:
            workout = await Workout.get_or_none(id=workout_id)
            if not workout:
                raise HTTPException(status_code=404, detail="Workout not found")
            
            update_data = data.model_dump(exclude_unset=True)
            if update_data:
                await workout.update_from_dict(update_data)
                await workout.save()
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    # Mantenha os métodos de Graphs (delete, get_all_workout_day, etc) 
    # Eles trabalham só com dados do Workout pai, então não precisam de muitas mudanças
    # exceto usar model_dump() se estiver migrando pydantic ou manter filtro simples.
    @staticmethod
    async def delete_workout(workout_id: str) -> None:
        # Igual ao original
        workout = await Workout.get_or_none(id=workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")
        await workout.delete()
        
    @staticmethod
    async def get_all_workout_day(user_id: str) -> list[date]:
        # Igual ao original
        workouts = await Workout.filter(user_id=user_id).all()
        workout_days = {w.start_time.date() for w in workouts}
        return sorted(list(workout_days))

    @staticmethod
    async def get_calories_by_all_days(user_id: str) -> list[tuple[date, float]]:
        # Igual ao original
        workouts = await Workout.filter(user_id=user_id).all()
        calories = {}
        for w in workouts:
            d = w.start_time.date()
            calories[d] = calories.get(d, 0) + w.total_calories_burned
        return sorted(calories.items())
    
    @staticmethod
    async def get_graphs_data(user_id: str) -> WorkoutGraphs:
        """
        Compila os dados de todos os treinos para alimentar os gráficos do Dashboard.
        """
        # Busca treinos ordenados por data
        workouts = await Workout.filter(user_id=user_id).order_by("start_time").all()

        calories_data = []
        duration_data = []
        
        # Dicionários auxiliares para agrupar por Tipo
        type_total_cals = {}
        type_count = {}

        for w in workouts:
            # Formatação de data simples (YYYY-MM-DD)
            # Se start_time for None (raro), pula
            if not w.start_time:
                continue
                
            date_str = w.start_time.strftime("%Y-%m-%d")

            # 1. Gráfico de Calorias
            calories_data.append(
                WorkoutCaloriesGraphPoint(
                    date=w.start_time, 
                    total_calories=w.total_calories_burned or 0.0
                )
            )

            # 2. Gráfico de Duração
            duration_min = 0.0
            if w.end_time:
                delta = w.end_time - w.start_time
                duration_min = round(delta.total_seconds() / 60, 2)
            
            duration_data.append(
                WorkoutDurationGraphPoint(
                    date=w.start_time, 
                    duration_minutes=duration_min
                )
            )

            # 3. Agrupamento por Tipo (Strength, Cardio, etc)
            t_type = w.type
            type_total_cals[t_type] = type_total_cals.get(t_type, 0.0) + (w.total_calories_burned or 0)
            type_count[t_type] = type_count.get(t_type, 0) + 1

        # Constrói lista de performance baseada nos agrupamentos
        performance_data = []
        for t_type, total_cal in type_total_cals.items():
            count = type_count[t_type]
            
            performance_data.append(
                WorkoutPerformanceByTypeGraphPoint(
                    date=datetime.now(),
                    type=t_type,
                    total_calories=total_cal,
                    duration_minutes=0.0,
                    workouts_count=count
                )
            )

        return WorkoutGraphs(
            calories_graph=calories_data,
            duration_graph=duration_data,
            performance_by_type_graph=performance_data
        )