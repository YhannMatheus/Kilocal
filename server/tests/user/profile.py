import pytest
from src.main import app as app


@pytest.mark.asyncio
async def test_profile_user(client):
    register_payload = {
        "email": "test@test.com.br",
        "name": "Test User",
        "password": "StrongP@ssw0rd",
        "height_cm": 175.5,
        "birth_date": "1990-01-01",
        "gender": "male",
    }
    
    register = await client.post("/register", json=register_payload)

    if register.status_code != 200:
        pytest.fail("Falha ao registrar o usuário para o teste de login.")
    # Agora, tentar logar com as credenciais corretas
    login = {
        "email": "test@test.com.br",
        "password": "StrongP@ssw0rd",
        "remember": False
    }

    login_response = await client.post("/login", json=login)
    if login_response.status_code != 200:
        pytest.fail("Falha ao logar o usuário para o teste de profile.")

    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/profile", headers=headers)
    assert response.status_code == 200