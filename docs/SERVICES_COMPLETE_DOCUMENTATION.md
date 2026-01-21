# ⚙️ Documentação Completa dos Serviços - KiloCal

> **Versão:** 1.0.1  
> **Última Atualização:** 20 de Janeiro de 2026  
> **Arquitetura:** Service Layer Pattern

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [UserService](#userservice)
3. [BodyAssessmentService](#bodyassessmentservice)
4. [WorkoutService](#workoutservice)
5. [SetService](#setservice)
6. [CaloricIntakeService](#caloricintakeservice)
7. [Calculations (Core)](#calculations-core)

---

## 🎯 Visão Geral

A camada de serviços contém a regra de negócio e isola o framework web (FastAPI) da lógica da aplicação.

### Estrutura de Arquivos:

```
src/services/
├── user_services.py              # Autenticação e Perfil
├── body_assessment_service.py    # Avaliações físicas e snapshot de métricas
├── workout_service.py            # Cabeçalhos de treino e dashboard
├── set_services.py               # Lógica de inserção de séries e cálculo calórico
├── caloric_intake_service.py     # Lógica nutricional (Nova)
├── exercise.py                   # CRUD de exercícios (Ainda não implementado serviço complexo)
└── session_services.py           # (Legado/Em refatoração)
```

---

## 👤 UserService
**Arquivo:** `user_services.py`

Responsável por:
- Registro de usuários (hash de senha).
- Login (geração de token via `src.core.auth`).
- Recuperação de perfil agregado (dados do usuário + últimos treinos + gráficos).

---

## 📏 BodyAssessmentService
**Arquivo:** `body_assessment_service.py`

O serviço mais "matemático" do sistema.
- **Snapshot Imutável**: Ao criar uma avaliação, ele calcula TUDO (BFP, TDEE, IMC) e salva no banco.
- **Gráficos**: Possui métodos otimizados para retornar dados em formato de série temporal (`created_at` vs `value`).

---

## 🏋️ WorkoutService
**Arquivo:** `workout_service.py`

Gerencia o "container" do treino.
- Cria o treino.
- Agrega estatísticas (soma calorias de todos os sets).
- Finaliza treinos (update `end_time`).
- Gera dados para o dashboard de performance física.

---

## 🔢 SetService
**Arquivo:** `set_services.py`

O "coração" do cálculo de esforço.
- Ao adicionar um set, ele invoca `WorkoutCalories.calculate_single_set_calories`.
- Atualiza atomicamente o total do workout pai.
- Busca o peso do usuário na avaliação mais recente para precisão calórica.

---

## 🥗 CaloricIntakeService
**Arquivo:** `caloric_intake_service.py` *NOVO*

Gerencia a entrada de alimentos.
- **Cálculo de macros**: Se o usuário enviar apenas protein/carb/fat, calcula as calorias totais (4-4-9).
- **Sumarização**: `get_daily_summary` agrega todas as refeições do dia para comparação Nutrition vs Training.

---

## 🧮 Calculations (Core)
**Local:** `src/core/calculations/`

Não são serviços, mas classes estáticas puras usadas pelos serviços.
1. **BodyMetrics**: Fórmulas de Navy Method, IMC, Idade.
2. **EnergyExpenditure**: Fórmulas de TMB (Mifflin-St Jeor) e TDEE.
3. **WorkoutCalories**: Tabela de METs e fórmulas de gasto por exercício.

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
