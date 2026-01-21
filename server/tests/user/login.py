import pytest
from src.main import app as app

base_url = "http://localhost:3000/api/v1/user"

@pytest.mark.asyncio
async def test_login_user(client):
    # Primeiro, registrar o usuário
    register_payload = {
        "email": "test@test.com.br",
        "name": "Test User",
        "password": "StrongP@ssw0rd",
        "height_cm": 175.5,
        "birth_date": "1990-01-01",
        "gender": "male",
    }
    
    response = await client.post("/register", json=register_payload)

    if response.status_code != 200:
        pytest.fail("Falha ao registrar o usuário para o teste de login.")
    # Agora, tentar logar com as credenciais corretas
    login = {
        "email": "test@test.com.br",
        "password": "StrongP@ssw0rd",
        "remember": False
    }

    response = await client.post("/login", json=login)
    assert response.status_code == 200
    