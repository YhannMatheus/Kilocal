# ⚙️ Documentação Completa dos Serviços - KiloCal

> **Versão:** 1.0.0  
> **Última Atualização:** 16 de Janeiro de 2026  
> **Arquitetura:** Service Layer Pattern

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura de Serviços](#arquitetura-de-serviços)
3. [UserService](#userservice)
4. [BodyAssessmentService](#bodyassessmentservice)
5. [WorkoutService](#workoutservice)
6. [ExerciseService](#exerciseservice)
7. [SetService](#setservice)
8. [SessionService](#sessionservice)
9. [Tratamento de Erros](#tratamento-de-erros)
10. [Validações](#validações)
11. [Boas Práticas](#boas-práticas)

---

## 🎯 Visão Geral

A camada de serviços (Service Layer) é responsável por toda a **lógica de negócio** da aplicação KiloCal. Esta camada:

- 🔹 Orquestra operações complexas entre múltiplos modelos
- 🔹 Executa validações de regras de negócio
- 🔹 Realiza cálculos automáticos (IMC, BFP, BMR, TDEE, etc.)
- 🔹 Trata exceções e retorna mensagens de erro amigáveis
- 🔹 Mantém o código das rotas limpo e focado em HTTP

### Estrutura de Arquivos:

```
src/services/
├── user_services.py              # Gerenciamento de usuários e autenticação
├── body_assessment_service.py    # Avaliações corporais e cálculos
├── workout_service.py            # Gerenciamento de treinos
├── exercise_service.py           # Gerenciamento de exercícios
├── set_service.py                # Gerenciamento de séries
└── session_services.py           # Gerenciamento de sessões
```

---

## 🏗️ Arquitetura de Serviços

### Fluxo de Dados:

```
┌──────────────────────────────────────────────────────────┐
│  ROUTE (Controller)                                      │
│  - Recebe requisição HTTP                                │
│  - Valida headers e autenticação                         │
│  - Extrai dados do request                               │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  SERVICE (Business Logic)                                │
│  - Valida regras de negócio                              │
│  - Executa cálculos complexos                            │
│  - Orquestra operações entre modelos                     │
│  - Trata exceções                                        │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  MODEL (ORM - Tortoise)                                  │
│  - Interação direta com banco de dados                   │
│  - Queries e persistência                                │
└──────────────────────────────────────────────────────────┘
```

### Padrão de Design:

Todos os serviços seguem o padrão **Static Class** com métodos `@staticmethod`:

```python
class ServiceName:
    @staticmethod
    async def method_name(params) -> ReturnType:
        # Lógica de negócio
        pass
```

**Vantagens:**
- ✅ Não requer instanciação
- ✅ Facilita uso direto em rotas
- ✅ Mantém estado em banco de dados, não em memória
- ✅ Simplicidade e clareza

---

## 👤 UserService

**Arquivo:** `src/services/user_services.py`

Gerencia operações relacionadas a usuários: registro, login, autenticação e perfil.

### Métodos:

#### `create_user(data: RegisterRequest) -> str`

Cria um novo usuário no sistema.

**Parâmetros:**
- `data` (RegisterRequest): Dados de registro do usuário
  - `name`: Nome completo
  - `email`: Email único
  - `password`: Senha (mínimo 8 caracteres)
  - `gender`: Sexo (`male` | `female`)
  - `birth_date`: Data de nascimento
  - `height_cm`: Altura em centímetros
  - `activity_level`: Nível de atividade física

**Retorno:**
- `str`: Token JWT de acesso

**Validações:**
1. ✅ Verifica se email já está em uso
2. ✅ Valida formato do email
3. ✅ Valida força da senha (mínimo 8 caracteres)
4. ✅ Hash da senha com bcrypt

**Exceções:**
- `400 Bad Request`: Email já em uso ou dados inválidos
- `500 Internal Server Error`: Erro ao criar usuário

**Exemplo:**

```python
from src.services.user_services import UserService
from src.types.schemas.auth import RegisterRequest

data = RegisterRequest(
    name="João Silva",
    email="joao@example.com",
    password="senha123",
    gender=GenderEnum.MALE,
    birth_date=date(1990, 1, 1),
    height_cm=175.0,
    activity_level=ActivityLevelEnum.MODERATE
)

token = await UserService.create_user(data)
```

---

#### `get_user(data: LoginRequest, remember: bool) -> str`

Realiza login e retorna token de acesso.

**Parâmetros:**
- `data` (LoginRequest): Credenciais de login
  - `email`: Email do usuário
  - `password`: Senha
- `remember` (bool): Se True, token expira em 7 dias; senão, 1 dia

**Retorno:**
- `str`: Token JWT de acesso

**Validações:**
1. ✅ Verifica se usuário existe
2. ✅ Verifica senha com bcrypt
3. ✅ Gera token JWT com informações do usuário

**Exceções:**
- `401 Unauthorized`: Email ou senha inválidos
- `500 Internal Server Error`: Erro ao processar login

**Exemplo:**

```python
from src.services.user_services import UserService
from src.types.schemas.auth import LoginRequest

data = LoginRequest(
    email="joao@example.com",
    password="senha123"
)

token = await UserService.get_user(data, remember=True)
```

---

#### `get_by_id(user_id: str) -> User`

Busca usuário por ID.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `User`: Objeto User do Tortoise ORM

**Exceções:**
- `404 Not Found`: Usuário não encontrado
- `500 Internal Server Error`: Erro ao buscar usuário

---

#### `get_user_profile(user_id: str) -> UserProfile`

Retorna perfil completo do usuário com treinos e gráficos de avaliação.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `UserProfile`: Objeto contendo:
  - `userData`: Informações do usuário
  - `workouts`: Lista de treinos
  - `body_graphs`: Gráficos de evolução corporal

**Operações:**
1. Busca usuário no banco
2. Carrega todos os treinos do usuário (paralelo)
3. Carrega gráficos de evolução corporal (paralelo)
4. Monta objeto UserProfile

**Exceções:**
- `404 Not Found`: Usuário não encontrado
- `500 Internal Server Error`: Erro ao buscar perfil

**Exemplo:**

```python
profile = await UserService.get_user_profile("uuid-do-usuario")

# Acessando dados
print(profile.userData.name)
print(f"Treinos: {len(profile.workouts)}")
print(f"IMC atual: {profile.body_graphs.bmi_graph[-1].value}")
```

---

## 📊 BodyAssessmentService

**Arquivo:** `src/services/body_assessment_service.py`

Gerencia avaliações corporais, cálculos de composição corporal e métricas de saúde.

### Métodos Principais:

#### `create_body_assessment(...) -> BodyAssessmentReed`

Cria nova avaliação corporal com cálculos automáticos.

**Parâmetros:**
- `user_id` (UUID): ID do usuário
- `user_gender` (GenderEnum): Sexo do usuário
- `user_birth_date` (date): Data de nascimento
- `user_activity_level` (ActivityLevelEnum): Nível de atividade
- `data` (BodyAssessmentCreate): Medidas corporais
  - `weight_kg`: Peso em kg (obrigatório)
  - `height_cm`: Altura em cm (obrigatório)
  - `waist_cm`: Cintura (opcional)
  - `hip_cm`: Quadril (opcional, obrigatório para mulheres no cálculo BFP)
  - `neck_cm`: Pescoço (opcional)
  - `chest_cm`: Peito (opcional)
  - `arm_cm`: Braço (opcional)
  - `thigh_cm`: Coxa (opcional)
  - Dobras cutâneas (todas opcionais)

**Retorno:**
- `BodyAssessmentReed`: Avaliação criada com resultados calculados
  - `id`: UUID da avaliação
  - `bmi`: IMC calculado
  - `bfp`: % de gordura calculado (se houver medidas)
  - `bmr`: Taxa metabólica basal
  - `tdee`: Gasto calórico total diário
  - `lean_mass_kg`: Massa magra
  - `fat_mass_kg`: Massa gorda
  - `created_at`: Data/hora da avaliação

**Cálculos Executados:**

1. **Idade**: Calculada a partir da data de nascimento
2. **BMI**: `peso / (altura_m)²`
3. **BFP** (% Gordura): Método Navy (se houver medidas)
   - Homens: cintura, pescoço, altura
   - Mulheres: cintura, quadril, pescoço, altura
4. **Massa Magra**: `peso × (1 - BFP/100)`
5. **Massa Gorda**: `peso × (BFP/100)`
6. **BMR**: Fórmula Mifflin-St Jeor
   - Homens: `10 × peso + 6.25 × altura - 5 × idade + 5`
   - Mulheres: `10 × peso + 6.25 × altura - 5 × idade - 161`
7. **TDEE**: `BMR × fator_atividade`
   - Sedentário: BMR × 1.2
   - Leve: BMR × 1.375
   - Moderado: BMR × 1.55
   - Alto: BMR × 1.725
   - Extra Ativo: BMR × 1.9

**Exceções:**
- `400 Bad Request`: Dados inválidos
- `500 Internal Server Error`: Erro ao criar avaliação

**Exemplo:**

```python
from src.services.body_assessment_service import BodyAssessmentService
from src.types.schemas.body_assessment import BodyAssessmentCreate

data = BodyAssessmentCreate(
    weight_kg=75.0,
    height_cm=175.0,
    waist_cm=85.0,
    hip_cm=95.0,
    neck_cm=38.0
)

assessment = await BodyAssessmentService.create_body_assessment(
    user_id=user.id,
    user_gender=user.gender,
    user_birth_date=user.birth_date,
    user_activity_level=user.activity_level,
    data=data
)

print(f"IMC: {assessment.bmi}")
print(f"% Gordura: {assessment.bfp}%")
print(f"TDEE: {assessment.tdee} kcal/dia")
```

---

#### `get_body_assessment(assessment_id: str) -> BodyAssessmentBase`

Recupera uma avaliação corporal específica.

**Parâmetros:**
- `assessment_id` (str): UUID da avaliação

**Retorno:**
- `BodyAssessmentBase`: Avaliação completa com todas as medidas e cálculos

**Exceções:**
- `404 Not Found`: Avaliação não encontrada
- `500 Internal Server Error`: Erro ao recuperar

---

#### `get_all_body_assessment_for_user_id(user_id: str) -> list[BodyAssessmentReed]`

Retorna todas as avaliações de um usuário.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `list[BodyAssessmentReed]`: Lista de avaliações resumidas

**Exceções:**
- `404 Not Found`: Nenhuma avaliação encontrada
- `500 Internal Server Error`: Erro ao recuperar

---

### Métodos de Gráficos:

Todos os métodos de gráficos seguem o mesmo padrão:

#### `bmi_for_date(user_id: str) -> list[GraphPoint]`
#### `bfp_for_date(user_id: str) -> list[GraphPoint]`
#### `tdee_for_date(user_id: str) -> list[GraphPoint]`
#### `weight_for_date(user_id: str) -> list[GraphPoint]`
#### `get_lean_mass_for_date(user_id: str) -> list[GraphPoint]`
#### `get_fat_mass_for_date(user_id: str) -> list[GraphPoint]`
#### `get_brm_for_date(user_id: str) -> list[GraphPoint]`

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `list[GraphPoint]`: Lista de pontos ordenados por data
  - `date`: Data/hora da avaliação
  - `value`: Valor da métrica

**Exemplo:**

```python
# Obter evolução de peso
weight_data = await BodyAssessmentService.weight_for_date(user_id)

for point in weight_data:
    print(f"{point.date}: {point.value} kg")
```

---

#### `get_body_assessment_graphs(user_id: str) -> BodyAssessmentGraphs`

Retorna todos os gráficos de evolução de uma vez (otimizado).

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `BodyAssessmentGraphs`: Objeto contendo todos os gráficos
  - `bfp_graph`: Evolução de % gordura
  - `bmi_graph`: Evolução de IMC
  - `tdee_graph`: Evolução de TDEE
  - `weight_graph`: Evolução de peso
  - `lean_mass_graph`: Evolução de massa magra
  - `fat_mass_graph`: Evolução de massa gorda

**Otimização:**
- Executa todas as 6 queries em paralelo usando `asyncio.gather()`

**Exemplo:**

```python
graphs = await BodyAssessmentService.get_body_assessment_graphs(user_id)

# Último peso
if graphs.weight_graph:
    latest_weight = graphs.weight_graph[-1].value
    print(f"Peso atual: {latest_weight} kg")
```

---

### Métodos Auxiliares (Privados):

#### `_calculate_body_fat_percentage(...) -> Optional[float]`

Calcula % de gordura usando método Navy.

**Lógica:**
1. Verifica se há medidas mínimas (cintura, pescoço)
2. Para mulheres, verifica se há medida de quadril
3. Aplica fórmula Navy específica por sexo
4. Retorna None se dados insuficientes

---

#### `_calculate_body_composition(...) -> tuple[Optional[float], Optional[float]]`

Calcula massa magra e gorda a partir do BFP.

**Retorno:**
- `(lean_mass_kg, fat_mass_kg)`

---

## 🏋️ WorkoutService

**Arquivo:** `src/services/workout_service.py`

Gerencia operações relacionadas a treinos.

### Métodos:

#### `create_workout(data: WorkoutCreate) -> str`

Cria um novo treino.

**Parâmetros:**
- `data` (WorkoutCreate): Dados do treino
  - `userid`: UUID do usuário
  - `name`: Nome do treino
  - `type`: Tipo de treino (strength, cardio, etc.)
  - `start_time`: Hora de início

**Retorno:**
- `str`: UUID do treino criado

**Exceções:**
- `500 Internal Server Error`: Erro ao criar treino

---

#### `get_all_user_workouts(user_id: str) -> list[WorkoutRead]`

Retorna todos os treinos de um usuário.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `list[WorkoutRead]`: Lista de treinos com exercícios básicos

**Otimização:**
- Usa `prefetch_related("exercises")` para evitar N+1 queries

**Exceções:**
- `404 Not Found`: Nenhum treino encontrado
- `500 Internal Server Error`: Erro ao recuperar

---

#### `get_workout_by_id(workout_id: str) -> WorkoutDetailed`

Retorna detalhes completos de um treino.

**Parâmetros:**
- `workout_id` (str): UUID do treino

**Retorno:**
- `WorkoutDetailed`: Treino com todos os exercícios e séries

**Exceções:**
- `404 Not Found`: Treino não encontrado
- `500 Internal Server Error`: Erro ao recuperar

---

#### `update_workout(workout_id: str, data: WorkoutUpdate) -> None`

Atualiza informações de um treino.

**Parâmetros:**
- `workout_id` (str): UUID do treino
- `data` (WorkoutUpdate): Campos a atualizar (parcial)
  - `name`: Novo nome (opcional)
  - `type`: Novo tipo (opcional)
  - `end_time`: Hora de término (opcional)

**Exceções:**
- `404 Not Found`: Treino não encontrado
- `500 Internal Server Error`: Erro ao atualizar

---

#### `delete_workout(workout_id: str) -> None`

Deleta um treino.

**Parâmetros:**
- `workout_id` (str): UUID do treino

**Exceções:**
- `404 Not Found`: Treino não encontrado
- `500 Internal Server Error`: Erro ao deletar

---

#### `get_all_workout_day(user_id: str) -> list[date]`

Retorna lista de datas únicas em que o usuário treinou.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `list[date]`: Datas ordenadas

**Exemplo:**

```python
workout_days = await WorkoutService.get_all_workout_day(user_id)
# [date(2026, 1, 10), date(2026, 1, 12), date(2026, 1, 15)]
```

---

#### `get_calories_by_all_days(user_id: str) -> list[tuple[date, float]]`

Retorna calorias queimadas por dia.

**Parâmetros:**
- `user_id` (str): UUID do usuário

**Retorno:**
- `list[tuple[date, float]]`: Lista de (data, calorias)

**Lógica:**
- Agrega calorias de múltiplos treinos no mesmo dia

---

## 💪 ExerciseService

**Arquivo:** `src/services/exercise_service.py`

Gerencia operações com exercícios.

### Métodos:

#### `create(data: ExerciseCreate) -> Exercisse`

Cria um novo exercício.

**Parâmetros:**
- `data` (ExerciseCreate): Dados do exercício
  - `workout_id`: UUID do treino
  - `name`: Nome do exercício (enum)
  - `type`: Tipo (strength, cardio, etc.)
  - `intensity`: Intensidade (low, moderate, high, very_high)

**Retorno:**
- `Exercisse`: Exercício criado

---

#### `get_by_id(exercise_id: UUID) -> Exercisse`

Busca exercício por ID.

---

#### `update(exercise_id: UUID, data: ExerciseUpdate) -> Exercisse`

Atualiza exercício.

---

#### `delete(exercise_id: UUID) -> None`

Deleta exercício.

---

## 🔢 SetService

**Arquivo:** `src/services/set_service.py`

Gerencia séries de exercícios.

### Métodos:

#### `create(exercise_id: UUID, user_id: UUID, user_weight_kg: float, data: SetCreate) -> Set`

Cria uma nova série.

**Parâmetros:**
- `exercise_id` (UUID): ID do exercício
- `user_id` (UUID): ID do usuário
- `user_weight_kg` (float): Peso do usuário (para cálculo de calorias)
- `data` (SetCreate): Dados da série
  - `reps`: Repetições (opcional)
  - `weight`: Peso usado (opcional)
  - `duration`: Duração em segundos (opcional)

**Retorno:**
- `Set`: Série criada

---

#### `get_by_id(set_id: UUID) -> Set`

Busca série por ID.

---

#### `update(set_id: UUID, data: SetUpdate) -> Set`

Atualiza série.

---

#### `delete(set_id: UUID) -> None`

Deleta série.

---

## 🔐 SessionService

**Arquivo:** `src/services/session_services.py`

Gerencia sessões de usuário (controle de autenticação).

### Métodos:

#### `create_session(user_id: str, remember: bool) -> SessionBase`

Cria ou atualiza sessão do usuário.

**Parâmetros:**
- `user_id` (str): UUID do usuário
- `remember` (bool): Sessão longa (7 dias) ou curta (1 dia)

**Retorno:**
- `SessionBase`: Sessão criada/atualizada

**Lógica:**
1. Busca sessão existente do usuário
2. Se existe, atualiza `expires_at`
3. Se não existe, cria nova sessão

**Exemplo:**

```python
session = await SessionService.create_session(
    user_id="uuid-do-usuario",
    remember=True
)
print(f"Sessão expira em: {session.expires_at}")
```

---

#### `get_session(userId: str) -> SessionBase`

Recupera e valida sessão do usuário.

**Parâmetros:**
- `userId` (str): UUID do usuário

**Retorno:**
- `SessionBase`: Sessão válida

**Validações:**
1. ✅ Verifica se sessão existe
2. ✅ Verifica se não expirou
3. ✅ Renova expiração automaticamente (sliding expiration)

**Exceções:**
- `404 Not Found`: Sessão não encontrada
- `401 Unauthorized`: Sessão expirada

---

## ⚠️ Tratamento de Erros

Todos os serviços seguem o padrão de tratamento de erros:

```python
@staticmethod
async def method_name(params) -> ReturnType:
    try:
        # Lógica de negócio
        result = await Model.operation()
        return result
        
    except HTTPException as e:
        # Re-lança exceções HTTP já tratadas
        raise e
        
    except DoesNotExist:
        # Trata not found do Tortoise ORM
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
        
    except ValueError as e:
        # Trata erros de validação
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )
        
    except Exception as e:
        # Log de erro e resposta genérica
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred"
        )
```

### Códigos HTTP Usados:

- `200 OK`: Operação bem-sucedida
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Não autenticado ou sessão expirada
- `403 Forbidden`: Sem permissão para acessar recurso
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

---

## ✅ Validações

### Validações de Usuário:

```python
# Email único
if await User.exists(email=data.email):
    raise HTTPException(400, "Email already in use")

# Formato de email
if not Validator.is_valid_email(data.email):
    raise HTTPException(400, "Invalid email format")

# Força da senha
if not Validator.is_strong_password(data.password):
    raise HTTPException(400, "Weak password")
```

### Validações de Avaliação Corporal:

```python
# Valores positivos
if data.weight_kg <= 0 or data.height_cm <= 0:
    raise ValueError("Weight and height must be positive")

# Medidas para cálculo BFP
if user_gender == GenderEnum.FEMALE and not data.hip_cm:
    return None  # BFP não calculado
```

### Validações de Treino:

```python
# Propriedade do recurso
if str(token.user_id) != str(workout.user_id):
    raise HTTPException(403, "No permission to access this workout")

# End time posterior a start time
if data.end_time and data.end_time < workout.start_time:
    raise HTTPException(400, "End time must be after start time")
```

---

## 🎯 Boas Práticas

### 1. Uso de Async/Await

Todos os métodos de serviço são assíncronos:

```python
# ✅ Correto
result = await UserService.create_user(data)

# ❌ Errado
result = UserService.create_user(data)  # Retorna coroutine
```

### 2. Operações em Paralelo

Use `asyncio.gather()` para operações independentes:

```python
# ✅ Otimizado (paralelo)
workouts, graphs = await asyncio.gather(
    Workout.filter(user_id=user_id).all(),
    BodyAssessmentService.get_body_assessment_graphs(user_id)
)

# ❌ Não otimizado (sequencial)
workouts = await Workout.filter(user_id=user_id).all()
graphs = await BodyAssessmentService.get_body_assessment_graphs(user_id)
```

### 3. Prefetch Related

Evite N+1 queries:

```python
# ✅ Otimizado
workouts = await Workout.filter(user_id=user_id).prefetch_related("exercises").all()
for workout in workouts:
    for exercise in workout.exercises:  # Já carregado
        print(exercise.name)

# ❌ N+1 Problem
workouts = await Workout.filter(user_id=user_id).all()
for workout in workouts:
    exercises = await workout.exercises.all()  # Query adicional!
```

### 4. Validações Explícitas

Sempre valide antes de processar:

```python
# ✅ Validação clara
if not user:
    raise HTTPException(404, "User not found")

# Continua processamento sabendo que user existe
```

### 5. Logs Informativos

Use print() para debugging (em desenvolvimento):

```python
print(f"❌ Erro ao criar avaliação corporal: {str(e)}")
print(f"✅ Avaliação criada com sucesso: {assessment.id}")
```

### 6. Retorno de Tipos Específicos

Use Pydantic schemas para retorno:

```python
# ✅ Tipado e validado
async def get_user(user_id: str) -> UserProfile:
    ...

# ❌ Tipo genérico
async def get_user(user_id: str) -> dict:
    ...
```

---

## 🔗 Relação com Outras Camadas

### Services → Models:

```python
# Service usa Model para persistência
user = await User.create(**data.dict())
```

### Routes → Services:

```python
# Route delega lógica para Service
@router.post("/register")
async def register(data: RegisterRequest):
    token = await UserService.create_user(data)
    return {"access_token": token}
```

### Services → Core (Calculations):

```python
# Service usa funções de cálculo
from src.core.calculations.body_metrics import BodyMetrics

bmi = BodyMetrics.calculate_bmi(weight_kg, height_cm)
```

---

## 📊 Métricas de Performance

### Operações Típicas:

| Operação                    | Complexidade | Queries DB | Tempo Médio |
|-----------------------------|--------------|------------|-------------|
| `create_user`               | O(1)         | 1          | ~50ms       |
| `get_user_profile`          | O(n)         | 3+         | ~200ms      |
| `create_body_assessment`    | O(1)         | 1          | ~30ms       |
| `get_all_user_workouts`     | O(n)         | 2          | ~100ms      |
| `get_body_assessment_graphs`| O(n)         | 6          | ~300ms      |

---

## 🛠️ Dependências

- **FastAPI**: Framework web
- **Tortoise ORM**: ORM assíncrono
- **Pydantic**: Validação de schemas
- **Asyncio**: Operações assíncronas
- **Core Calculations**: Fórmulas matemáticas

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
**Versão do Documento:** 1.0.0
