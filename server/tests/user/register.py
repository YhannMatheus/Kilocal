import pytest
from src.main import app as app

base_url = "http://localhost:3000/api/v1/user"

@pytest.mark.asyncio
async def test_register_user(client):
    payload = {
        "email": "test@test.com.br", 
        "name": "Test User",
        "password": "StrongP@ssw0rd",
        "height_cm": 175.5,
        "birth_date": "1990-01-01",
        "gender": "male",
    }
    response = await client.post("/register", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_register_duplicate_user(client):
    payload ={
        "email": "test@test.com.br",
        "name": "Test User",
        "password": "StrongP@ssw0rd",
        "height_cm": 175.5,
        "birth_date":"1990-01-01",
        "gender":"male"
    }

    await client.post("/register", json=payload)
    response = await client.post("/register", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use"