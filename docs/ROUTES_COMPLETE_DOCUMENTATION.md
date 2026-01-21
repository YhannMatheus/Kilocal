# 🚀 Documentação Completa das Rotas - KiloCal API

> **Versão:** 1.0.1  
> **Última Atualização:** 20 de Janeiro de 2026  
> **Base URL (Produção):** `https://kilocal-8fy9.onrender.com/api/v1`  
> **Base URL (Desenvolvimento):** `http://localhost:8000/api/v1`

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Rotas de Usuário](#rotas-de-usuário)
4. [Rotas de Avaliação Corporal](#rotas-de-avaliação-corporal)
5. [Rotas de Treino](#rotas-de-treino)
6. [Rotas de Nutrição](#rotas-de-nutrição)
7. [Códigos de Resposta HTTP](#códigos-de-resposta-http)
8. [Tratamento de Erros](#tratamento-de-erros)
9. [Exemplos de Uso](#exemplos-de-uso)

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
│   └── /graph/{search_type}                 # GET - Dados para gráficos de evolução (protegido)
│
├── /workouts                                # Treinos
│   ├── /                                    # POST - Criar novo treino (protegido)
│   ├── /                                    # GET - Listar treinos do usuário (protegido)
│   ├── /{workout_id}                        # GET - Detalhes completos de um treino (protegido)
│   ├── /{workout_id}                        # PUT - Atualizar cabeçalho/Finalizar treino (protegido)
│   ├── /{workout_id}                        # DELETE - Apagar treino e seus sets (protegido)
│   ├── /graphs/stats                        # GET - Dados estatísticos gerais (protegido)
│   │
│   ├── /{workout_id}/sets                   # POST - Adicionar Set (exercício/série) (protegido)
│   ├── /sets/{set_id}                       # PUT - Atualizar Set (protegido)
│   └── /sets/{set_id}                       # DELETE - Remover Set (protegido)
│
└── /nutrition                               # Nutrição e Calorias
    ├── /meal                                # POST - Registrar nova refeição (protegido)
    ├── /summary/today                       # GET - Resumo de macros de hoje (protegido)
    └── /summary/{query_date}                # GET - Resumo de macros por data (protegido)
```

---

## 🔐 Autenticação

Todas as rotas (exceto `/register`, `/login` e `/health`) requerem um token JWT válido.

**Header Obrigatório:**
```
Authorization: Bearer <seu_token_jwt>
```

---

## 👤 Rotas de Usuário

### POST `/user/register`

Registra um novo usuário.

### POST `/user/login`

Autentica usuário e retorna token JWT.

### GET `/user/profile`

Retorna perfil completo do usuário autenticado.

---

## 📏 Rotas de Avaliação Corporal

Base URL: `/body-assessment`

### POST `/`

Cria uma nova avaliação corporal. O sistema calcula automaticamente métricas como IMC, % Gordura, TMB e TDEE com base nos dados fornecidos.

**Body:**
```json
{
  "weight_kg": 75.5,
  "height_cm": 175,
  "waist_cm": 80,
  "neck_cm": 38,
  "hip_cm": 95,            // Obrigatório para mulheres (fórmula Navy)
  "chest_cm": 100,         // Opcional
  ...
  "fold_abdominal": 15,    // Opcional
  "fold_chest": 10,        // Opcional
  ...
}
```

### GET `/`

Retorna o histórico de avaliações do usuário.

### GET `/{assessment_id}`

Detalhes completos de uma avaliação.

### GET `/graph/{search_type}`

Retorna dados para gráficos.

**Path Parameters:**
- `search_type` (Enum):
  - `weight`: Evolução do Peso
  - `bfp`: Evolução do % Gordura
  - `bmi`: Evolução do IMC
  - `bmr`: Evolução da Taxa Metabólica
  - `tdee`: Evolução do Gasto Calórico
  - `lean_fat_mass`: Evolução da composição corporal

---

## 🏋️ Rotas de Treino

Base URL: `/workouts`

### POST `/`

Cria um cabeçalho de treino (e.g. "Peito e Tríceps").

**Body:**
```json
{
  "user_id": "uuid",
  "name": "Treino A",
  "type": "strength",     // strength, cardio, flexibility, etc.
  "start_time": "2026-01-20T10:00:00"
}
```

### POST `/{workout_id}/sets`

Adiciona uma série/exercício ao treino.

**Body:**
```json
{
  "exercise_id": "uuid",
  "reps": 12,
  "weight": 20.0,
  "duration": null,
  "distance": null
}
```

### PUT `/sets/{set_id}`

Atualiza uma série (ex: corrigiu a carga).

### DELETE `/sets/{set_id}`

Remove uma série.

### GET `/`

Lista resumo dos treinos do usuário.

### GET `/{workout_id}`

Retorna o treino completo, com todos os exercícios e séries e suas estatísticas de calorias.

### GET `/graphs/stats`

Retorna estatísticas agregadas para dashboard de treinos.

---

## 🥗 Rotas de Nutrição

Base URL: `/nutrition`

### POST `/meal`

Registra uma refeição.

**Body:**
```json
{
  "name": "Almoço",
  "protein_grams": 40.0,
  "carbs_grams": 50.0,
  "fats_grams": 15.0,
  "calories_consumed": 500  // Opcional (calculado auto se omitido)
}
```

### GET `/summary/today`

Retorna macros e calorias totais de hoje.

**Resposta:**
```json
{
  "date": "2026-01-20",
  "total_calories": 2500.0,
  "total_protein": 180.0,
  "total_carbs": 300.0,
  "total_fats": 70.0,
  "entries": [...]
}
```

### GET `/summary/{query_date}`

Retorna o resumo nutricional de uma data específica.

---

## 🚦 Códigos de Resposta HTTP

- **200 OK:** Sucesso.
- **201 Created:** Recurso criado com sucesso.
- **204 No Content:** Sucesso mas sem conteúdo de retorno (delete).
- **400 Bad Request:** Erro de validação nos dados enviados.
- **401 Unauthorized:** Token ausente ou inválido.
- **403 Forbidden:** Token válido mas sem permissão para o recurso.
- **404 Not Found:** Recurso não encontrado.
- **500 Internal Server Error:** Erro no servidor.

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
