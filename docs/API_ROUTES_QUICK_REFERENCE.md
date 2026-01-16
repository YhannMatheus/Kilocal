# 📋 Referência Rápida - Rotas da API KiloCal

> **Base URL (Desenvolvimento):** `http://localhost:8000/api/v1`  
> **Base URL (Produção):** `https://kilocal-8fy9.onrender.com/api/v1`

---

## 🔓 Rotas Públicas (Sem Autenticação)

### Health Check
```
GET /api/v1/
```
Verifica se a API está rodando.

---

### Registro de Usuário
```
POST /api/v1/user/register
```

**Body:**
```json
{
  "email": "usuario@example.com",
  "name": "Nome Completo",
  "password": "senha123",
  "birth_date": "1990-01-01",
  "height_cm": 175.0,
  "gender": "male",
  "activity_level": "moderate"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Login
```
POST /api/v1/user/login
```

**Body:**
```json
{
  "email": "usuario@example.com",
  "password": "senha123",
  "remember": true
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 🔐 Rotas Protegidas (Requerem Token JWT)

> **Header obrigatório:** `Authorization: Bearer {access_token}`

---

## 👤 Usuários

### Perfil do Usuário
```
GET /api/v1/user/profile
```

**Resposta:** Perfil completo com treinos e gráficos corporais

---

## 📊 Avaliações Corporais

### Criar Avaliação
```
POST /api/v1/body-assessment/
```

**Body:**
```json
{
  "weight_kg": 75.0,
  "height_cm": 175.0,
  "waist_cm": 85.0,
  "hip_cm": 95.0,
  "neck_cm": 38.0,
  "chest_cm": 100.0,
  "arm_cm": 35.0,
  "thigh_cm": 60.0
}
```

**Resposta:** Avaliação criada com cálculos automáticos (IMC, BFP, BMR, TDEE)

---

### Listar Todas as Avaliações
```
GET /api/v1/body-assessment/
```

**Resposta:** Array de avaliações resumidas

---

### Buscar Avaliação Específica
```
GET /api/v1/body-assessment/{assessment_id}
```

**Resposta:** Avaliação completa com todas as medidas

---

### Dados para Gráficos
```
GET /api/v1/body-assessment/graph/{user_id}/{scrach}
```

**Parâmetros de URL:**
- `user_id`: UUID do usuário
- `scrach`: Tipo de métrica
  - `BFP` - Percentual de gordura
  - `BMI` - Índice de massa corporal
  - `BMR` - Taxa metabólica basal
  - `TDEE` - Gasto calórico total
  - `WEIGTH` - Peso corporal

**Resposta:** Array de pontos `[{date, value}]`

---

## 🏋️ Treinos

### Criar Treino
```
POST /api/v1/workout/
```

**Body:**
```json
{
  "userid": "uuid-do-usuario",
  "name": "Treino de Peito e Tríceps",
  "type": "strength",
  "start_time": "2026-01-16T10:00:00Z"
}
```

**Tipos de treino:**
- `strength` - Musculação
- `cardio` - Cardio
- `flexibility` - Flexibilidade
- `hiit` - HIIT
- `functional` - Funcional
- `other` - Outro

---

### Listar Treinos do Usuário
```
GET /api/v1/workout/{userid}
```

**Resposta:** Array de treinos com resumo de exercícios

---

### Detalhes Completos do Treino
```
GET /api/v1/workout/detail/{workoutid}
```

**Resposta:** Treino completo com exercícios e séries

---

### Atualizar Treino
```
PUT /api/v1/workout/{workoutid}
```

**Body (todos opcionais):**
```json
{
  "name": "Novo Nome",
  "type": "cardio",
  "end_time": "2026-01-16T11:30:00Z"
}
```

---

### Dias de Treino
```
GET /api/v1/workout/days/{userid}
```

**Resposta:** Array de datas únicas `["2026-01-10", "2026-01-12"]`

---

## 📝 Exemplos de Uso

### 1. Fluxo Completo de Registro e Primeira Avaliação

```bash
# 1. Registrar usuário
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "name": "João Silva",
    "password": "senha123",
    "birth_date": "1990-01-01",
    "height_cm": 175.0,
    "gender": "male",
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

# 3. Ver perfil
curl -X GET "http://localhost:8000/api/v1/user/profile" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 2. Criar e Gerenciar Treino

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123",
    "remember": true
  }' | jq -r '.access_token')

# 2. Criar treino
WORKOUT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/workout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userid": "uuid-do-usuario",
    "name": "Treino A - Peito",
    "type": "strength",
    "start_time": "2026-01-16T10:00:00Z"
  }')

WORKOUT_ID=$(echo $WORKOUT_RESPONSE | jq -r '.workout_id')

# 3. Finalizar treino
curl -X PUT "http://localhost:8000/api/v1/workout/$WORKOUT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "end_time": "2026-01-16T11:30:00Z"
  }'

# 4. Ver detalhes
curl -X GET "http://localhost:8000/api/v1/workout/detail/$WORKOUT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⚠️ Códigos de Resposta

| Código | Significado | Quando ocorre |
|--------|-------------|---------------|
| 200 | OK | Requisição bem-sucedida |
| 400 | Bad Request | Dados inválidos |
| 401 | Unauthorized | Token inválido/ausente |
| 403 | Forbidden | Sem permissão |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro no servidor |

---

## 🔑 Enums Importantes

### GenderEnum
- `male`
- `female`

### ActivityLevelEnum
- `sedentary` - Sedentário
- `light` - Levemente ativo
- `moderate` - Moderadamente ativo
- `high` - Muito ativo
- `extra_active` - Extra ativo
- `athlete` - Atleta

### TrainingTypeEnum (Workout)
- `strength` - Musculação
- `cardio` - Cardio
- `flexibility` - Flexibilidade
- `hiit` - HIIT
- `functional` - Funcional
- `other` - Outro

### BioStatusType (Gráficos)
- `BFP` - Body Fat Percentage
- `BMI` - Body Mass Index
- `BMR` - Basal Metabolic Rate
- `TDEE` - Total Daily Energy Expenditure
- `WEIGTH` - Weight

---

## 📚 Documentação Completa

Para documentação detalhada, consulte:
- [ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md) - Documentação completa das rotas
- [SERVICES_COMPLETE_DOCUMENTATION.md](./SERVICES_COMPLETE_DOCUMENTATION.md) - Lógica de negócio
- [DATABASE_COMPLETE_DOCUMENTATION.md](./DATABASE_COMPLETE_DOCUMENTATION.md) - Estrutura do banco

---

## 🌐 URLs de Acesso

### Desenvolvimento:
- API: http://localhost:8000/api/v1
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Produção:
- API: https://kilocal-8fy9.onrender.com/api/v1
- Swagger: https://kilocal-8fy9.onrender.com/docs
- ReDoc: https://kilocal-8fy9.onrender.com/redoc

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Email:** yhann.mendes@poraygua.com.br  
**Versão:** 1.0.0  
**Data:** 16 de Janeiro de 2026
