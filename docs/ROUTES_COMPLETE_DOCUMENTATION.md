# 🚀 Documentação Completa das Rotas - KiloCal API

> **Versão:** 1.0.0  
> **Última Atualização:** 16 de Janeiro de 2026  
> **Base URL (Produção):** `https://kilocal-8fy9.onrender.com/api/v1`  
> **Base URL (Desenvolvimento):** `http://localhost:8000/api/v1`

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Rotas de Usuário](#rotas-de-usuário)
4. [Rotas de Avaliação Corporal](#rotas-de-avaliação-corporal)
5. [Rotas de Treino](#rotas-de-treino)
6. [Códigos de Resposta HTTP](#códigos-de-resposta-http)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Exemplos de Uso](#exemplos-de-uso)

---

## 🎯 Visão Geral

A API KiloCal segue o padrão **RESTful** e está organizada em módulos:

### Estrutura de Rotas Completa:

```
/api/v1
├── /                                        # GET - Health check (público)
│
├── /user                                    # Gerenciamento de usuários
│   ├── /register                            # POST - Registro de novo usuário (público)
│   ├── /login                               # POST - Login e autenticação (público)
│   └── /profile                             # GET - Perfil completo do usuário (protegido)
│
├── /body-assessment                         # Avaliações corporais
│   ├── /                                    # POST - Criar nova avaliação (protegido)
│   ├── /                                    # GET - Listar todas avaliações (protegido)
│   ├── /{assessment_id}                     # GET - Buscar avaliação específica (protegido)
│   └── /graph/{user_id}/{scrach}            # GET - Dados para gráficos de evolução (protegido)
│
└── /workout                                 # Treinos
    ├── /                                    # POST - Criar novo treino (protegido)
    ├── /{userid}                            # GET - Listar todos treinos do usuário (protegido)
    ├── /detail/{workoutid}                  # GET - Detalhes completos de um treino (protegido)
    ├── /{workoutid}                         # PUT - Atualizar treino existente (protegido)
    └── /days/{userid}                       # GET - Listar dias que o usuário treinou (protegido)
```

### Resumo de Endpoints:

| Método | Rota Completa | Descrição | Auth |
|--------|---------------|-----------|------|
| GET | `/api/v1/` | Health check da API | ❌ |
| POST | `/api/v1/user/register` | Registrar novo usuário | ❌ |
| POST | `/api/v1/user/login` | Login (retorna JWT) | ❌ |
| GET | `/api/v1/user/profile` | Perfil do usuário autenticado | ✅ |
| POST | `/api/v1/body-assessment/` | Criar avaliação corporal | ✅ |
| GET | `/api/v1/body-assessment/` | Listar avaliações do usuário | ✅ |
| GET | `/api/v1/body-assessment/{id}` | Buscar avaliação específica | ✅ |
| GET | `/api/v1/body-assessment/graph/{user_id}/{type}` | Dados de gráficos | ✅ |
| POST | `/api/v1/workout/` | Criar novo treino | ✅ |
| GET | `/api/v1/workout/{userid}` | Listar treinos do usuário | ✅ |
| GET | `/api/v1/workout/detail/{workoutid}` | Detalhes do treino | ✅ |
| PUT | `/api/v1/workout/{workoutid}` | Atualizar treino | ✅ |
| GET | `/api/v1/workout/days/{userid}` | Dias de treino | ✅ |

### Características:

- ✅ **RESTful**: Verbos HTTP semânticos (GET, POST, PUT, DELETE)
- ✅ **JWT Authentication**: Autenticação via Bearer Token
- ✅ **JSON**: Todas as requisições e respostas em JSON
- ✅ **CORS**: Configurado para web e mobile
- ✅ **Pydantic Validation**: Validação automática de entrada
- ✅ **OpenAPI/Swagger**: Documentação interativa em `/docs`

---

## 🔐 Autenticação

### Fluxo de Autenticação:

```
1. Usuário faz POST /user/register ou /user/login
   ↓
2. API valida credenciais
   ↓
3. API gera JWT token
   ↓
4. Cliente recebe token
   ↓
5. Cliente envia token em todas as requisições protegidas
   Header: Authorization: Bearer {token}
```

### JWT Token:

**Estrutura:**
```json
{
  "user_id": "uuid",
  "role": "user | admin",
  "exp": 1234567890,  // Timestamp de expiração
  "iat": 1234567890   // Timestamp de emissão
}
```

**Expiração:**
- Com `remember=true`: 7 dias
- Sem `remember` ou `false`: 1 dia

**Middleware de Autenticação:**

A API possui middleware global que:
1. Extrai token do header `Authorization`
2. Valida token JWT
3. Decodifica informações do usuário
4. Disponibiliza dados do token para as rotas

**Rotas Públicas** (sem autenticação):
- `GET /`
- `POST /user/register`
- `POST /user/login`

**Rotas Protegidas** (requerem autenticação):
- Todas as outras rotas

---

## 👤 Rotas de Usuário

### POST `/api/v1/user/register`

Registra um novo usuário no sistema.

**URL Completa:** `POST /api/v1/user/register`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "string (email válido, único)",
  "name": "string",
  "password": "string (min 8 caracteres)",
  "birth_date": "YYYY-MM-DD",
  "height_cm": "float (> 0, < 300)",
  "gender": "male | female",
  "activity_level": "sedentary | light | moderate | high | extra_active | athlete"
}
```

**Validações:**
- ✅ Email único no sistema
- ✅ Formato de email válido
- ✅ Senha com no mínimo 8 caracteres
- ✅ Data de nascimento válida (idade mínima 13 anos)
- ✅ Altura maior que 0

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Erros:**
- `400 Bad Request`: Email já em uso ou dados inválidos
  ```json
  {
    "detail": "Email already in use"
  }
  ```
- `500 Internal Server Error`: Erro ao processar registro

**Exemplo:**

```bash
curl -X POST "http://localhost:8000/api/v1/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "name": "João Silva",
    "password": "senha123",
    "birth_date": "1990-01-01",
    "height_cm": 175.0,
    "gender": "male",
    "activity_level": "moderate"
  }'
```

---

### POST `/api/v1/user/login`

Realiza login e retorna token de acesso.

**URL Completa:** `POST /api/v1/user/login`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "string (email válido)",
  "password": "string",
  "remember": "boolean (opcional, default: false)"
}
```

**Parâmetros do Body:**
- `email` (string, obrigatório): Email do usuário
- `password` (string, obrigatório): Senha
- `remember` (boolean, opcional): Se `true`, token expira em 7 dias; se `false`, 1 dia

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Erros:**
- `401 Unauthorized`: Email ou senha inválidos
  ```json
  {
    "detail": "Invalid email or password"
  }
  ```
- `500 Internal Server Error`: Erro ao processar login

**Exemplo:**

```bash
curl -X POST "http://localhost:8000/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123",
    "remember": true
  }'
```

---

### GET `/api/v1/user/profile`

Retorna perfil completo do usuário autenticado com histórico de treinos e gráficos corporais.

**URL Completa:** `GET /api/v1/user/profile`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Resposta (200):**
```json
{
  "userData": {
    "id": "uuid",
    "email": "string",
    "name": "string",
    "birth_date": "YYYY-MM-DD",
    "height_cm": "float",
    "gender": "male | female",
    "activity_level": "sedentary | light | moderate | high | extra_active | athlete"
  },
  "workouts": [
    {
      "name": "string",
      "type": "strength | cardio | flexibility | hiit | functional | other",
      "start_time": "datetime",
      "total_calories_burned": "float",
      "duration_minutes": "float",
      "exercises": [
        {
          "id": "uuid",
          "name": "string",
          "type": "strength | cardio | flexibility | balance",
          "intensity": "low | moderate | high | very_high"
        }
      ]
    }
  ],
  "body_graphs": {
    "bfp_graph": [
      {
        "date": "datetime",
        "value": "float"
      }
    ],
    "bmi_graph": [...],
    "tdee_graph": [...],
    "weight_graph": [...],
    "lean_mass_graph": [...],
    "fat_mass_graph": [...]
  }
}
```

**Erros:**
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Usuário não encontrado
- `500 Internal Server Error`: Erro ao buscar perfil

**Exemplo:**

```bash
curl -X GET "http://localhost:8000/api/v1/user/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---
api/v1/body-assessment/`

Cria uma nova avaliação corporal com cálculos automáticos.

**URL Completa:** `POST /api/v1/body-assessment/`
### POST `/body-assessment/`

Cria uma nova avaliação corporal com cálculos automáticos.

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body:**
```json
{
  "weight_kg": "float (obrigatório)",
  "height_cm": "float (obrigatório)",
  "waist_cm": "float (opcional)",
  "hip_cm": "float (opcional, obrigatório para mulheres no cálculo BFP)",
  "chest_cm": "float (opcional)",
  "neck_cm": "float (opcional)",
  "arm_cm": "float (opcional)",
  "thigh_cm": "float (opcional)",
  "fold_chest": "float (opcional)",
  "fold_abdominal": "float (opcional)",
  "fold_thigh": "float (opcional)",
  "fold_triceps": "float (opcional)",
  "fold_subscapular": "float (opcional)",
  "fold_suprailiac": "float (opcional)",
  "fold_midaxillary": "float (opcional)"
}
```

**Cálculos Automáticos:**

O sistema calcula automaticamente:
- **BMI** (Índice de Massa Corporal)
- **BFP** (% de Gordura - se houver medidas suficientes)
- **BMR** (Taxa Metabólica Basal)
- **TDEE** (Gasto Calórico Total Diário)
- **Massa Magra**
- **Massa Gorda**

**Resposta (200):**
```json
{
  "id": "uuid",
  "bfp": "float | null",
  "bmi": "float",
  "bmr": "float",
  "tdee": "float",
  "lean_mass_kg": "float | null",
  "fat_mass_kg": "float | null",
  "created_at": "datetime"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `400 Bad Request`: Dados inválidos
- `500 Internal Server Error`: Erro ao criar avaliação

**Exemplo:**

```bash
curl -X POST "http://localhost:8000/api/v1/body-assessment/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "weight_kg": 75.0,
    "height_cm": 175.0,
    "waist_cm": 85.0,
    "hip_cm": 95.0,
    "neck_cm": 38.0
  }'
```

---api/v1/body-assessment/`

Retorna todas as avaliações corporais do usuário autenticado.

**URL Completa:** `GET /api/v1/body-assessment/`

Retorna todas as avaliações corporais do usuário autenticado.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Resposta (200):**
```json
[
  {
    "id": "uuid",
    "bfp": "float | null",
    "bmi": "float",
    "bmr": "float",
    "tdee": "float",
    "lean_mass_kg": "float | null",
    "fat_mass_kg": "float | null",
    "created_at": "datetime"
  }
]
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `500 Internal Server Error`: Erro ao buscar avaliações

**Exemplo:**

```bash
curl -X GET "http://localhost:8000/api/v1/body-assessment/" \
  -H "Authorization: Bearer {token}"
```api/v1/body-assessment/{assessment_id}`

Retorna uma avaliação corporal específica com todos os detalhes.

**URL Completa:** `GET /api/v1/body-assessment/{assessment_id}`

### GET `/body-assessment/{assessment_id}`

Retorna uma avaliação corporal específica com todos os detalhes.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `assessment_id` (UUID): ID da avaliação

**Resposta (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "weight_kg": "float",
  "height_cm": "float",
  "waist_cm": "float | null",
  "hip_cm": "float | null",
  "chest_cm": "float | null",
  "neck_cm": "float | null",
  "arm_cm": "float | null",
  "thigh_cm": "float | null",
  "fold_chest": "float | null",
  "fold_abdominal": "float | null",
  "fold_thigh": "float | null",
  "fold_triceps": "float | null",
  "fold_subscapular": "float | null",
  "fold_suprailiac": "float | null",
  "fold_midaxillary": "float | null",
  "bfp": "float | null",
  "bmi": "float",
  "bmr": "float",
  "tdee": "float",
  "lean_mass_kg": "float | null",
  "fat_mass_kg": "float | null",
  "created_at": "datetime"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão para acessar esta avaliação
- `404 Not Found`: Avaliação não encontrada
- `500 Intapi/v1/body-assessment/graph/{user_id}/{scrach}`

Retorna dados de gráfico para uma métrica específica ao longo do tempo.

**URL Completa:** `GET /api/v1/body-assessment/graph/{user_id}/{scrach}`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `user_id` (UUID): ID do usuário
- `scrach` (string): Tipo de métrica (BioStatusType enum)

**Path Parameters:**
- `user_id` (UUID): ID do usuário
- `screach` (string): Tipo de métrica
  - `BFP`: Percentual de gordura corporal
  - `TDEE`: Gasto calórico diário total
  - `WEIGTH`: Peso corporal
  - `BMI`: Índice de massa corporal
  - `BMR`: Taxa metabólica basal

**Resposta (200):**
```json
[
  {
    "date": "datetime",
    "value": "float"
  },
  {
    "date": "datetime",
    "value": "float"
  }
]
```

**Erros:**
- `400 Bad Request`: Tipo de métrica inválido
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão
- `500 Internal Server Error`: Erro ao buscar dados

**Exemplo:**

```bash
# Obter evolução de peso
curl -X GET "http://localhost:8000/api/v1/body-assessment/graph/{user_id}/WEIGTH" \
  -H "Authorization: Bearer {token}"
```api/v1/workout/`

Cria um novo treino para o usuário autenticado.

**URL Completa:** `POST /api/v1/workout/`

## 🏋️ Rotas de Treino

### POST `/workout/`

Cria um novo treino para o usuário autenticado.

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body:**
```json
{
  "userid": "uuid",
  "name": "string",
  "type": "strength | cardio | flexibility | hiit | functional | other",
  "start_time": "datetime (ISO 8601)"
}
```

**Validações:**
- ✅ Usuário só pode criar treino para si mesmo
- ✅ Nome é obrigatório
- ✅ Tipo de treino é obrigatório

**Resposta (200):**
```json
{
  "message": "Workout created successfully",
  "workout_id": "uuid"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão para criar treino para outro usuário
- `500 Internal Server Error`: Erro ao criar treino

**Exemplo:**

```bash
curl -X POST "http://localhost:8000/api/v1/workout/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "userid": "uuid-do-usuario",
    "name": "Treino de Peito e Tríceps",
    "type": "strength",
    "startapi/v1/workout/{userid}`

Retorna todos os treinos de um usuário.

**URL Completa:** `GET /api/v1/workout/{userid}`

---

### GET `/workout/{userid}`

Retorna todos os treinos de um usuário.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `userid` (UUID): ID do usuário

**Resposta (200):**
```json
[
  {
    "name": "string",
    "type": "strength | cardio | flexibility | hiit | functional | other",
    "start_time": "datetime",
    "total_calories_burned": "float",
    "duration_minutes": "float",
    "exercises": [
      {
        "id": "uuid",
        "name": "string",
        "type": "strength | cardio | flexibility | balance",
        "intensity": "low | moderate | high | very_high"
      }
    ]
  }
]
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Nenhum treino encontrado
- `500 Internal Server Error`: Erro ao buscar treinos

**Exemplo:**

```bash
curl -X GEapi/v1/workout/detail/{workoutid}`

Retorna detalhes completos de um treino específico.

**URL Completa:** `GET /api/v1/workout/detail/{workoutid}`

---

### GET `/workout/detail/{workoutid}`

Retorna detalhes completos de um treino específico.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `workoutid` (UUID): ID do treino

**Resposta (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "type": "strength | cardio | flexibility | hiit | functional | other",
  "start_time": "datetime",
  "end_time": "datetime | null",
  "total_calories_burned": "float",
  "duration_minutes": "float",
  "exercises": [
    {
      "id": "uuid",
      "name": "string",
      "type": "strength | cardio | flexibility | balance",
      "intensity": "low | moderate | high | very_high",
      "calories_burned": "float",
      "sets": [
        {
          "id": "uuid",
          "reps": "integer | null",
          "weight": "float | null",
          "duration": "integer | null",
          "calories_burned": "float",
          "created_at": "datetime"
        }
      ]
    }
  ],
  "create_at": "datetime"
}
```

**Erros:**api/v1/workout/{workoutid}`

Atualiza informações de um treino existente.

**URL Completa:** `PUT /api/v1/workout/{workoutid}`
- `404 Not Found`: Treino não encontrado
- `500 Internal Server Error`: Erro ao buscar detalhes

---

### PUT `/workout/{workoutid}`

Atualiza informações de um treino existente.

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Path Parameters:**
- `workoutid` (UUID): ID do treino

**Body (todos os campos são opcionais):**
```json
{
  "name": "string (opcional)",
  "type": "strength | cardio | flexibility | hiit | functional | other (opcional)",
  "end_time": "datetime (opcional)"
}
```

**Resposta (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "type": "string",
  "start_time": "datetime",
  "end_time": "datetime | null",
  "total_calories_burned": "float",
  "duration_minutes": "float",
  "exercises": [...],
  "create_at": "datetime"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão
- `404 Not Found`: Treino não encontrado
- `500 Internal Server Error`: Erro ao atualizar

**Exemplo:**

```bash
curl -X PUT "http://localhost:8000/api/v1/workout/{workoutid}" \
  -H "Authorization: Bearer {token}" \
  -H "Contapi/v1/workout/days/{userid}`

Retorna todos os dias únicos em que o usuário treinou.

**URL Completa:** `GET /api/v1/workout/days/{userid}`
  }'
```

---

### GET `/workout/days/{userid}`

Retorna todos os dias únicos em que o usuário treinou.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `userid` (UUID): ID do usuário

**Resposta (200):**
```json
[
  "2026-01-10",
  "2026-01-12",
  "2026-01-15"
]
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Usuário não tem permissão
- `500 Internal Server Error`: Erro ao buscar dias

**Exemplo:**

```bash
curl -X GET "http://localhost:8000/api/v1/workout/days/{userid}" \
  -H "Authorization: Bearer {token}"
```

---

## 🔢 Códigos de Resposta HTTP

### Sucesso (2xx):

| Código | Descrição            | Uso                                    |
|--------|----------------------|----------------------------------------|
| 200    | OK                   | Requisição bem-sucedida                |
| 201    | Created              | Recurso criado com sucesso             |

### Erro do Cliente (4xx):

| Código | Descrição            | Uso                                    |
|--------|----------------------|----------------------------------------|
| 400    | Bad Request          | Dados inválidos na requisição          |
| 401    | Unauthorized         | Token inválido, ausente ou expirado    |
| 403    | Forbidden            | Sem permissão para acessar recurso     |
| 404    | Not Found            | Recurso não encontrado                 |
| 422    | Unprocessable Entity | Erro de validação Pydantic             |

### Erro do Servidor (5xx):

| Código | Descrição            | Uso                                    |
|--------|----------------------|----------------------------------------|
| 500    | Internal Server Error| Erro interno do servidor               |

---

## ⚠️ Tratamento de Erros

### Formato de Erro Padrão:

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Exemplos de Erros:

**Token Inválido:**
```json
{
  "detail": "Invalid token or token has expired"
}
```

**Permissão Negada:**
```json
{
  "detail": "You do not have permission to access this workout"
}
```

**Recurso Não Encontrado:**
```json
{
  "detail": "Workout not found"
}
```

**Validação Pydantic:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 📝 Exemplos de Uso

### Fluxo Completo: Registro → Login → Criar Avaliação

```bash
# 1. Registrar usuário
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123",
    "gender": "male",
    "birth_date": "1990-01-01",
    "height_cm": 175.0,
    "activity_level": "moderate"
  }' | jq -r '.access_token')

# 2. Criar avaliação corporal
curl -X POST "http://localhost:8000/api/v1/body-assessment/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "weight_kg": 75.0,
    "height_cm": 175.0,
    "waist_cm": 85.0,
    "neck_cm": 38.0
  }'

# 3. Ver perfil completo
curl -X GET "http://localhost:8000/api/v1/user/profile" \
  -H "Authorization: Bearer $TOKEN"
```

### Fluxo de Treino:

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/user/login?remember=true" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }' | jq -r '.access_token')

# 2. Criar treino
WORKOUT_ID=$(curl -s -X POST "http://localhost:8000/api/v1/workout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userid": "uuid-do-usuario",
    "name": "Treino de Peito",
    "type": "strength",
    "start_time": "2026-01-16T10:00:00Z"
  }' | jq -r '.workout_id')

# 3. Finalizar treino
curl -X PUT "http://localhost:8000/api/v1/workout/$WORKOUT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "end_time": "2026-01-16T11:30:00Z"
  }'

# 4. Ver detalhes do treino
curl -X GET "http://localhost:8000/api/v1/workout/detail/$WORKOUT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔗 Middlewares

### CORS Middleware:

Configurado para aceitar requisições de:
- `http://localhost:3000` (desenvolvimento local)
- `https://kilocal-8fy9.onrender.com` (produção)

**Configuração:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://kilocal-8fy9.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Auth Middleware:

Middleware global que:
1. Intercepta todas as requisições
2. Verifica se rota requer autenticação
3. Extrai e valida token JWT
4. Disponibiliza dados do usuário para a rota

**Rotas Excluídas:**
- `/`
- `/user/register`
- `/user/login`
- `/docs`
- `/openapi.json`

---

## 📚 Documentação Interativa

### Swagger UI:

Acesse: `http://localhost:8000/docs`

- ✅ Interface interativa para testar endpoints
- ✅ Visualização de schemas
- ✅ Autenticação via interface
- ✅ Exemplos de requisição/resposta

### ReDoc:

Acesse: `http://localhost:8000/redoc`

- ✅ Documentação formatada
- ✅ Melhor para leitura
- ✅ Navegação por tags

---

## 🛠️ Estrutura de Rotas

```python
# src/routes/user.py
router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login", response_model=Token)
async def login(data: LoginRequest, remember: bool = False) -> Token:
    # Implementação
    pass

# src/routes/body_assessment.py
router = APIRouter(prefix="/body-assessment", tags=["Body Assessment"])

@router.post("/", response_model=BodyAssessmentReed)
async def create_body_assessment(data: BodyAssessmentCreate, authorization:str = Header(...)):
    # Implementação
    pass

# src/routes/workout.py
router = APIRouter(prefix="/workout", tags=["Workout"])

@router.post("/")
async def create_workout(data: WorkoutCreate, authorization:str = Header(...)):
    # Implementação
    pass
```

---

## 🎯 Boas Práticas

### 1. Sempre Enviar Token:

```bash
# ✅ Correto
curl -H "Authorization: Bearer {token}" ...

# ❌ Errado
curl ...  # Receberá 401 Unauthorized
```

### 2. Validar Permissões:

Usuários só podem acessar seus próprios recursos:

```python
# Verificação automática nas rotas
if str(token.user_id) != str(resource.user_id):
    raise HTTPException(403, "No permission")
```

### 3. Usar UUIDs Corretos:

```bash
# ✅ UUID válido
"550e8400-e29b-41d4-a716-446655440000"

# ❌ Formato inválido
"123"
```

### 4. Formato de Datas:

Use ISO 8601:

```json
{
  "birth_date": "1990-01-01",
  "start_time": "2026-01-16T10:00:00Z"
}
```

---

## 📊 Performance

### Otimizações Implementadas:

- ✅ **Prefetch Related**: Carrega relacionamentos em uma query
- ✅ **Operações Paralelas**: Usa `asyncio.gather()` quando possível
- ✅ **Connection Pooling**: Pool de conexões do Tortoise ORM
- ✅ **Índices**: Índices otimizados no banco de dados

### Tempos Médios de Resposta:

| Endpoint                  | Tempo Médio |
|---------------------------|-------------|
| POST /user/register       | ~100ms      |
| POST /user/login          | ~80ms       |
| GET /user/profile         | ~250ms      |
| POST /body-assessment/    | ~50ms       |
| GET /body-assessment/     | ~80ms       |
| POST /workout/            | ~40ms       |
| GET /workout/{userid}     | ~120ms      |

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
**Versão do Documento:** 1.0.0
