from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.connection import configure_database
from src.core.middlewares.auth_middleware import AuthMiddleware

from src.routes import user
from src.routes import body_assessment
from src.routes import workout

app = FastAPI(
    title="KiloCal API",
    description="API para acompanhamento de treinos e cálculo de calorias",
    version="1.0.0",
    root_path="/api/v1",
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

print(f"""
API Rodando!
Documentação: http://localhost:8000/docs
propriedade de: Yhann Matheus de dio miranda mendes
contato: yhann.mendes@poraygua.com.br
versão: {app.version}
""")

