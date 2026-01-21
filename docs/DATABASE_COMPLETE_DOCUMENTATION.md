# 🗄️ Documentação Completa do Banco de Dados - KiloCal

> **Versão:** 1.0.1  
> **Última Atualização:** 20 de Janeiro de 2026  
> **Sistema de Banco de Dados:** PostgreSQL  
> **ORM:** Tortoise ORM 0.25.3

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Schema](#estrutura-do-schema)
3. [Tabelas Detalhadas](#tabelas-detalhadas)
   - [users](#tabela-users)
   - [body_assessments](#tabela-body_assessments)
   - [workouts](#tabela-workouts)
   - [exercises](#tabela-exercises)
   - [sets](#tabela-sets)
   - [caloric_intakes](#tabela-caloric_intakes)
4. [Relacionamentos](#relacionamentos)

---

## 🎯 Visão Geral

O banco de dados KiloCal foi projetado para gerenciar o ciclo de vida atlético do usuário:

- **Usuários**: Informações pessoais e configurações.
- **Avaliações**: Histórico de composição corporal (snapshots imutáveis).
- **Treinos**: Arquitetura `Workout` -> `Set` -> `Exercise`.
- **Nutrição**: Registro de macronutrientes e calorias.

---

## 🏗️ Estrutura do Schema

### Tabela `users`
Armazena os dados de autenticação e perfil básico.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador único |
| `email` | VARCHAR | Email único |
| `hashed_password` | VARCHAR | Senha criptografada |
| `name` | VARCHAR | Nome completo |
| `gender` | ENUM | Male/Female |
| `activity_level` | ENUM | Sedentary, Moderate, Active... |
| `created_at` | DATETIME | Data de registro |

### Tabela `body_assessments`
Registros históricos da composição corporal.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador |
| `user_id` | UUID (FK) | Relacionamento com User |
| `weight_kg` | FLOAT | Peso no momento da avaliação |
| `bfp` | FLOAT | % de Gordura calculado |
| `tdee` | FLOAT | Gasto Calórico Total calculado |
| `lean_mass_kg` | FLOAT | Massa Magra calculada |
| `fat_mass_kg` | FLOAT | Massa Gorda calculada |
| `created_at` | DATETIME | Data da avaliação |
| *Medidas...* | FLOAT | Diversos campos de circunferências e dobras |

### Tabela `workouts`
Cabeçalho de uma sessão de treino.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador |
| `user_id` | UUID (FK) | Quem treinou |
| `name` | VARCHAR | Nome (ex: "Peito A") |
| `type` | ENUM | Strength, Cardio, CrossFit... |
| `start_time` | DATETIME | Início do treino |
| `end_time` | DATETIME | Fim do treino |
| `total_calories` | FLOAT | Soma das calorias dos sets |

### Tabela `exercises`
Biblioteca de exercícios disponíveis.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador |
| `name` | VARCHAR | Nome do exercício |
| `target_muscle` | ENUM | Chest, Back, Legs... |
| `is_system_default` | BOOLEAN | (Novo) Se é exercício padrão do sistema |
| `created_by` | UUID (FK) | (Novo) Se foi criado por usuário (custom) |

### Tabela `sets`
Os exercícios realizados dentro de um treino.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador |
| `workout_id` | UUID (FK) | Pertence a qual treino |
| `exercise_id` | UUID (FK) | Qual exercício foi feito |
| `reps` | INT | Repetições |
| `weight` | FLOAT | Carga (kg) |
| `calories_burned` | FLOAT | Gasto calórico desta série específica |

### Tabela `caloric_intakes`
Registro de refeições.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID (PK) | Identificador |
| `user_id` | UUID (FK) | Quem comeu |
| `name` | VARCHAR | Nome da refeição |
| `date` | DATE | Data do registro |
| `protein_grams` | FLOAT | Proteínas (g) |
| `carbs_grams` | FLOAT | Carboidratos (g) |
| `fats_grams` | FLOAT | Gorduras (g) |
| `calories_consumed` | FLOAT | Calorias totais |

---

## 🔗 Relacionamentos

1. **User (1) <-> (N) BodyAssessment**: Um usuário tem várias avaliações.
2. **User (1) <-> (N) Workout**: Um usuário tem vários treinos.
3. **User (1) <-> (N) CaloricIntake**: Um usuário tem vários registros de refeição.
4. **Workout (1) <-> (N) Set**: Um treino é composto por várias séries.
5. **Exercise (1) <-> (N) Set**: Um exercício pode estar em várias séries de vários treinos.

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
