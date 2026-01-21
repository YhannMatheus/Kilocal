import asyncio
import sys
import os

# Adiciona o diretório atual ao PYTHONPATH se executado de dentro de server/
sys.path.append(os.getcwd())

from tortoise import Tortoise
from src.core.database.db_config import TORTOISE_ORM
from src.types.models.exercise import Exercise
from src.core.database.seed.exercises_default import DEFAULT_EXERCISES

async def seed_exercises():
    print("Iniciando seed de exercícios...")
    
    try:
        # Initialize DB
        await Tortoise.init(config=TORTOISE_ORM)
        
        count_new = 0
        count_existing = 0
        
        for exercise_data in DEFAULT_EXERCISES:
            # Check if exists by name AND is_system_default=True
            exists = await Exercise.filter(
                name=exercise_data["name"], 
                is_system_default=True
            ).exists()
            
            if not exists:
                await Exercise.create(
                    **exercise_data,
                    is_system_default=True
                )
                print(f"Criado: {exercise_data['name']}")
                count_new += 1
            else:
                count_existing += 1
                
        print(f"\nSeed concluído!")
        print(f"Novos exercícios: {count_new}")
        print(f"Existentes: {count_existing}")
        
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(seed_exercises())
