from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.connection import configure_database
from src.core.middlewares.auth_middleware import AuthMiddleware
from src.core.config import settings

from src.routes import user
from src.routes import body_assessment
from src.routes import workout

app = FastAPI(
    title="KiloCal API",
    description="API para acompanhamento de treinos e cálculo de calorias",
    version="1.0.0",
    root_path="/api/v1",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", # desenvolvimento local
                   "https://kilocal-8fy9.onrender.com", # produção -> TODO >>> conseguir um domínio próprio
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

database = configure_database(app)

app.include_router(user.router)
app.include_router(body_assessment.router)
app.include_router(workout.router)
#app.include_router(exercise.router)
#app.include_router(set.router)
#app.include_router(caloric_intake.router)


@app.get("/")
def root():
    return {"message": "KiloCal API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    base_url = "https://kilocal-8fy9.onrender.com" if settings.STAGE == "PROD" else "http://localhost:8000"
    print(f"\nAPI Rodando em modo: {settings.STAGE}")
    print(f"Documentação: {base_url}/api/v1/docs\n")

