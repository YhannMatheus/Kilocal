import pytest
import asyncio
from tortoise import Tortoise
from src.types.models.user import User
from httpx import AsyncClient, ASGITransport
from src.main import app

# Configuração simplificada para SQLite em memória
TEST_TORTOISE_ORM = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": [
                "src.types.models.user", 
                "src.types.models.workout", 
                "src.types.models.exercise", 
                "src.types.models.sets", 
                "src.types.models.body_assessments",
                "src.types.models.caloric_intakes",
                "src.types.models.session",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}

@pytest.fixture(scope="session")
def event_loop():
    """Garante um único loop para a sessão, evitando erros no Windows."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def initialize_db(event_loop):
    """Inicializa o banco em memória e gera as tabelas automaticamente."""
    await Tortoise.init(config=TEST_TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.fixture(autouse=True)
async def clear_db():
    """No SQLite em memória isso é opcional entre testes, mas mantém a organização."""
    yield

@pytest.fixture
async def client():
    """Cliente HTTP para os testes de integração."""
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://localhost:3000/api/v1/user"
    ) as ac:
        yield ac