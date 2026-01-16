# 🗄️ Documentação Completa do Banco de Dados - KiloCal

> **Versão:** 1.0.0  
> **Última Atualização:** 16 de Janeiro de 2026  
> **Sistema de Banco de Dados:** PostgreSQL  
> **ORM:** Tortoise ORM 0.25.3

---

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Diagrama de Relacionamentos (ERD)](#diagrama-de-relacionamentos-erd)
3. [Tabelas Detalhadas](#tabelas-detalhadas)
   - [users](#-users-usuários)
   - [body_assessments](#-body_assessments-avaliações-corporais)
   - [workouts](#️-workouts-treinos)
   - [exercises](#-exercises-exercícios)
   - [sets](#-sets-séries)
   - [caloric_intakes](#️-caloric_intakes-ingestão-calórica)
4. [Relacionamentos e Integridade](#relacionamentos-e-integridade)
5. [Índices e Performance](#índices-e-performance)
6. [Enumerações (Enums)](#enumerações-enums)
7. [Regras de Negócio](#regras-de-negócio)
8. [Migrações](#migrações)
9. [Fluxos de Dados](#fluxos-de-dados)

---

## 🎯 Visão Geral

O banco de dados KiloCal foi projetado para gerenciar:

- **Usuários**: Informações pessoais, autenticação e configurações
- **Avaliações Corporais**: Histórico de medidas, composição corporal e métricas calculadas
- **Treinos**: Registro completo de workouts, exercícios e séries
- **Ingestão Calórica**: Controle de alimentação e macronutrientes

### Características Técnicas:
- ✅ **Integridade Referencial**: CASCADE DELETE em todos os relacionamentos
- ✅ **UUIDs**: Todos os IDs são UUIDs v4
- ✅ **Timestamps**: Auditoria completa com `created_at` e `updated_at`
- ✅ **Enums**: Validação de valores através de enumerações
- ✅ **Campos Nullable**: Flexibilidade para dados opcionais
- ✅ **Índices Otimizados**: Performance em queries comuns

---

## 🗺️ Diagrama de Relacionamentos (ERD)

```
┌─────────────────────────────────────────┐
│             USERS                       │
├─────────────────────────────────────────┤
│ PK  id                 UUID             │
│ 🔑  email              VARCHAR(255)     │
│     name               VARCHAR(255)     │
│     hashed_password    VARCHAR(255)     │
│     birth_date         DATE             │
│     height_cm          FLOAT            │
│     goal               FLOAT            │
│     gender             ENUM             │
│     activity_level     ENUM             │
│     role               ENUM             │
│     activates_at       DATETIME         │
│     created_at         DATETIME         │
│     updated_at         DATETIME         │
└─────────────────────────────────────────┘
           │
           │ 1:N
           ├──────────────────────────────────────┬──────────────────────────┐
           │                                      │                          │
           ▼                                      ▼                          ▼
┌─────────────────────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────┐
│       BODY_ASSESSMENTS                  │ │    WORKOUTS              │ │   CALORIC_INTAKES        │
├─────────────────────────────────────────┤ ├──────────────────────────┤ ├──────────────────────────┤
│ PK  id                   UUID           │ │ PK  id            UUID   │ │ PK  id          UUID     │
│ FK  user_id              UUID           │ │ FK  user_id       UUID   │ │ FK  user_id     UUID     │
│     weight_kg            FLOAT          │ │     name          VARCHAR│ │     calories    FLOAT    │
│     height_cm            FLOAT          │ │     type          ENUM   │ │     protein_g   FLOAT    │
│     waist_cm             FLOAT          │ │     start_time    DATETIME│ │    carbs_g      FLOAT    │
│     hip_cm               FLOAT          │ │     end_time      DATETIME│ │    fat_g        FLOAT    │
│     chest_cm             FLOAT          │ │     total_calories FLOAT │ │     created_at  DATETIME │
│     neck_cm              FLOAT          │ │     create_at     DATETIME│ └──────────────────────────┘
│     arm_cm               FLOAT          │ └──────────────────────────┘
│     thigh_cm             FLOAT          │            │
│     fold_chest           FLOAT          │            │ 1:N
│     fold_abdominal       FLOAT          │            ▼
│     fold_thigh           FLOAT          │ ┌──────────────────────────┐
│     fold_triceps         FLOAT          │ │      EXERCISES           │
│     fold_subscapular     FLOAT          │ ├──────────────────────────┤
│     fold_suprailiac      FLOAT          │ │ PK  id          UUID     │
│     fold_midaxillary     FLOAT          │ │ FK  workout_id  UUID     │
│     bfp                  FLOAT (calc)   │ │     name        ENUM     │
│     bmi                  FLOAT (calc)   │ │     type        ENUM     │
│     bmr                  FLOAT (calc)   │ │     intensity   ENUM     │
│     tdee                 FLOAT (calc)   │ │     calories    FLOAT    │
│     lean_mass_kg         FLOAT (calc)   │ │     created_at  DATETIME │
│     fat_mass_kg          FLOAT (calc)   │ └──────────────────────────┘
│     created_at           DATETIME       │            │
└─────────────────────────────────────────┘            │ 1:N
                                                       ▼
                                            ┌──────────────────────────┐
                                            │        SETS              │
                                            ├──────────────────────────┤
                                            │ PK  id          UUID     │
                                            │ FK  exercise_id UUID     │
                                            │     reps        INTEGER  │
                                            │     weight      FLOAT    │
                                            │     duration    INTEGER  │
                                            │     calories    FLOAT    │
                                            │     created_at  DATETIME │
                                            └──────────────────────────┘
```

---

## 📋 Tabelas Detalhadas

### 🧑 **users** (Usuários)

Armazena informações dos usuários cadastrados na aplicação.

#### Estrutura da Tabela:

| Campo             | Tipo          | Descrição                                      | Constraints                  |
|-------------------|---------------|------------------------------------------------|------------------------------|
| `id`              | UUID          | Identificador único do usuário                 | PRIMARY KEY                  |
| `email`           | VARCHAR(255)  | Email do usuário                               | UNIQUE, INDEX, NOT NULL      |
| `name`            | VARCHAR(255)  | Nome completo do usuário                       | NOT NULL                     |
| `hashed_password` | VARCHAR(255)  | Senha criptografada (bcrypt)                   | NOT NULL                     |
| `birth_date`      | DATE          | Data de nascimento                             | NOT NULL                     |
| `height_cm`       | FLOAT         | Altura em centímetros                          | DEFAULT 0.0                  |
| `goal`            | FLOAT         | Meta de peso/calorias do usuário               | NULLABLE                     |
| `gender`          | ENUM          | Sexo: `male`, `female`                         | NOT NULL                     |
| `activity_level`  | ENUM          | Nível de atividade física                      | NOT NULL                     |
| `role`            | ENUM          | Papel do usuário: `user`, `admin`              | DEFAULT 'user'               |
| `activates_at`    | DATETIME      | Data de ativação da conta                      | NULLABLE                     |
| `created_at`      | DATETIME      | Data de criação do registro                    | AUTO_NOW_ADD                 |
| `updated_at`      | DATETIME      | Data da última atualização                     | AUTO_NOW                     |

#### Relacionamentos:
- **1:N** com `body_assessments` - Um usuário tem várias avaliações corporais
- **1:N** com `workouts` - Um usuário tem vários treinos
- **1:N** com `caloric_intakes` - Um usuário tem vários registros de ingestão calórica

#### Enums Utilizados:
- `GenderEnum`: `male`, `female`
- `ActivityLevelEnum`: `sedentary`, `light`, `moderate`, `high`, `extra_active`, `athlete`
- `RoleEnum`: `user`, `admin`

#### Regras de Validação:
- Email deve ser único no sistema
- Senha armazenada com hash bcrypt
- Altura deve ser maior que 0
- Data de nascimento deve indicar idade mínima de 13 anos

#### Índices:
- INDEX em `email` para performance em login

#### Modelo Tortoise ORM:

```python
from tortoise import Model, fields
from uuid import uuid4
from src.types.enums.user import GenderEnum, ActivityLevelEnum, RoleEnum

class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    hashed_password = fields.CharField(max_length=255)
    birth_date = fields.DateField()
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)
    height_cm = fields.FloatField(default=0.0)
    goal = fields.FloatField(null=True)
    gender = fields.CharEnumField(GenderEnum)
    activity_level = fields.CharEnumField(ActivityLevelEnum)
    activates_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
```

---

### 📊 **body_assessments** (Avaliações Corporais)

Armazena avaliações físicas e medidas corporais do usuário ao longo do tempo com cálculos automáticos.

#### Estrutura da Tabela:

| Campo                | Tipo      | Descrição                              | Constraints                  |
|----------------------|-----------|----------------------------------------|------------------------------|
| `id`                 | UUID      | Identificador único da avaliação       | PRIMARY KEY                  |
| `user_id`            | UUID      | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE  |
| **MEDIDAS BÁSICAS**  |           |                                        |                              |
| `weight_kg`          | FLOAT     | Peso em quilogramas                    | NOT NULL                     |
| `height_cm`          | FLOAT     | Altura em centímetros                  | NOT NULL                     |
| **CIRCUNFERÊNCIAS**  |           |                                        |                              |
| `waist_cm`           | FLOAT     | Circunferência da cintura (cm)         | NULLABLE                     |
| `hip_cm`             | FLOAT     | Circunferência do quadril (cm)         | NULLABLE                     |
| `chest_cm`           | FLOAT     | Circunferência do peito (cm)           | NULLABLE                     |
| `neck_cm`            | FLOAT     | Circunferência do pescoço (cm)         | NULLABLE                     |
| `arm_cm`             | FLOAT     | Circunferência do braço (cm)           | NULLABLE                     |
| `thigh_cm`           | FLOAT     | Circunferência da coxa (cm)            | NULLABLE                     |
| **DOBRAS CUTÂNEAS**  |           |                                        |                              |
| `fold_chest`         | FLOAT     | Dobra cutânea peitoral (mm)            | NULLABLE                     |
| `fold_abdominal`     | FLOAT     | Dobra cutânea abdominal (mm)           | NULLABLE                     |
| `fold_thigh`         | FLOAT     | Dobra cutânea da coxa (mm)             | NULLABLE                     |
| `fold_triceps`       | FLOAT     | Dobra cutânea do tríceps (mm)          | NULLABLE                     |
| `fold_subscapular`   | FLOAT     | Dobra cutânea subescapular (mm)        | NULLABLE                     |
| `fold_suprailiac`    | FLOAT     | Dobra cutânea supra-ilíaca (mm)        | NULLABLE                     |
| `fold_midaxillary`   | FLOAT     | Dobra cutânea axilar média (mm)        | NULLABLE                     |
| **RESULTADOS CALCULADOS** |      |                                        |                              |
| `bfp`                | FLOAT     | % de Gordura (Body Fat %)              | NULLABLE, CALCULADO          |
| `bmi`                | FLOAT     | IMC (Body Mass Index)                  | NULLABLE, CALCULADO          |
| `bmr`                | FLOAT     | Taxa Metabólica Basal (kcal/dia)       | NULLABLE, CALCULADO          |
| `tdee`               | FLOAT     | Gasto Energético Total (kcal/dia)      | NULLABLE, CALCULADO          |
| `lean_mass_kg`       | FLOAT     | Massa Magra (kg)                       | NULLABLE, CALCULADO          |
| `fat_mass_kg`        | FLOAT     | Massa Gorda (kg)                       | NULLABLE, CALCULADO          |
| `created_at`         | DATETIME  | Data/hora da avaliação                 | AUTO_NOW_ADD                 |

#### Relacionamentos:
- **N:1** com `users` - Várias avaliações pertencem a um usuário

#### Cálculos Automáticos:

Ao criar uma avaliação corporal, o sistema calcula automaticamente:

1. **BMI (Índice de Massa Corporal)**
   - Fórmula: `peso_kg / (altura_m)²`

2. **BFP (Percentual de Gordura)**
   - Método Navy (circunferências)
   - Requer: cintura, pescoço e altura
   - Para mulheres: também requer quadril

3. **BMR (Taxa Metabólica Basal)**
   - Fórmula: Mifflin-St Jeor
   - Considera: sexo, idade, peso, altura

4. **TDEE (Gasto Calórico Total Diário)**
   - Fórmula: BMR × fator_atividade
   - Baseado no nível de atividade do usuário

5. **Massa Magra e Gorda**
   - Com base no BFP calculado
   - Massa Magra: `peso × (1 - BFP/100)`
   - Massa Gorda: `peso × (BFP/100)`

#### Regras de Validação:
- Peso e altura são obrigatórios
- Valores devem ser positivos
- Medidas são opcionais, mas afetam cálculos
- BFP só é calculado se houver medidas suficientes

#### Índices:
- INDEX em `user_id` (foreign key)
- INDEX em `created_at` para ordenação temporal

#### Modelo Tortoise ORM:

```python
from tortoise import Model, fields

class BodyAssessment(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="body_assessments", on_delete=fields.CASCADE)
    
    # Medidas básicas
    weight_kg = fields.FloatField(description="Peso total no dia da avaliação")
    height_cm = fields.FloatField(description="Altura no momento")
    
    # Circunferências
    waist_cm = fields.FloatField(null=True)
    hip_cm = fields.FloatField(null=True)
    chest_cm = fields.FloatField(null=True)
    neck_cm = fields.FloatField(null=True)
    arm_cm = fields.FloatField(null=True)
    thigh_cm = fields.FloatField(null=True)
    
    # Dobras cutâneas
    fold_chest = fields.FloatField(null=True)
    fold_abdominal = fields.FloatField(null=True)
    fold_thigh = fields.FloatField(null=True)
    fold_triceps = fields.FloatField(null=True)
    fold_subscapular = fields.FloatField(null=True)
    fold_suprailiac = fields.FloatField(null=True)
    fold_midaxillary = fields.FloatField(null=True)
    
    # Resultados calculados
    bfp = fields.FloatField(null=True)
    bmi = fields.FloatField(null=True)
    bmr = fields.FloatField(null=True)
    tdee = fields.FloatField(null=True)
    lean_mass_kg = fields.FloatField(null=True)
    fat_mass_kg = fields.FloatField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "body_assessments"
```

---

### 🏋️ **workouts** (Treinos)

Armazena os treinos criados pelos usuários.

#### Estrutura da Tabela:

| Campo                     | Tipo         | Descrição                              | Constraints                  |
|---------------------------|--------------|----------------------------------------|------------------------------|
| `id`                      | UUID         | Identificador único do treino          | PRIMARY KEY                  |
| `user_id`                 | UUID         | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE  |
| `name`                    | VARCHAR(255) | Nome do treino                         | NOT NULL                     |
| `type`                    | ENUM         | Tipo de treino                         | NOT NULL                     |
| `start_time`              | DATETIME     | Hora de início do treino               | NOT NULL                     |
| `end_time`                | DATETIME     | Hora de término do treino              | NULLABLE                     |
| `total_calories_burned`   | FLOAT        | Total de calorias queimadas            | DEFAULT 0.0                  |
| `create_at`               | DATETIME     | Data de criação do registro            | AUTO_NOW_ADD                 |

#### Relacionamentos:
- **N:1** com `users` - Vários treinos pertencem a um usuário
- **1:N** com `exercises` - Um treino tem vários exercícios

#### Propriedade Computada:
- `duration_minutes`: Calculada dinamicamente como `(end_time - start_time) / 60`

#### Enums Utilizados:
- `TrainingTypeEnum`: `strength`, `cardio`, `flexibility`, `hiit`, `functional`, `other`

#### Regras de Validação:
- Nome é obrigatório
- Tipo de treino é obrigatório
- `end_time` deve ser posterior a `start_time`

#### Índices:
- INDEX em `user_id` (foreign key)
- INDEX em `start_time` para ordenação cronológica

#### Modelo Tortoise ORM:

```python
from tortoise import fields, Model
from src.types.enums.workout import TrainingTypeEnum

class Workout(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="workouts", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    type = fields.CharEnumField(TrainingTypeEnum)
    total_calories_burned = fields.FloatField(default=0.0)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)
    create_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "workouts"
    
    @property
    def duration_minutes(self) -> float:
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60.0
        return 0.0
```

---

### 💪 **exercises** (Exercícios)

Armazena os exercícios dentro de cada treino.

#### Estrutura da Tabela:

| Campo               | Tipo          | Descrição                                    | Constraints                  |
|---------------------|---------------|----------------------------------------------|------------------------------|
| `id`                | UUID          | Identificador único do exercício             | PRIMARY KEY                  |
| `workout_id`        | UUID          | Referência ao treino                         | FOREIGN KEY, CASCADE DELETE  |
| `name`              | ENUM          | Nome do exercício                            | NOT NULL                     |
| `type`              | ENUM          | Tipo de exercício                            | NOT NULL                     |
| `intensity`         | ENUM          | Intensidade do exercício                     | NOT NULL                     |
| `calories_burned`   | FLOAT         | Calorias queimadas no exercício              | DEFAULT 0.0                  |
| `created_at`        | DATETIME      | Data de criação                              | AUTO_NOW_ADD                 |

#### Relacionamentos:
- **N:1** com `workouts` - Vários exercícios pertencem a um treino
- **1:N** com `sets` - Um exercício tem várias séries

#### Enums Utilizados:
- `ExercisseNameEnum`: Lista extensiva de exercícios predefinidos
- `ExerciseTypeEnum`: `strength`, `cardio`, `flexibility`, `balance`
- `IntensityLevelEnum`: `low`, `moderate`, `high`, `very_high`

#### Índices:
- INDEX em `workout_id` (foreign key)

#### Modelo Tortoise ORM:

```python
from tortoise import fields, Model
from src.types.enums.exercise import ExerciseTypeEnum, IntensityLevelEnum, ExercisseNameEnum

class Exercisse(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharEnumField(ExercisseNameEnum)
    workout = fields.ForeignKeyField("models.Workout", related_name="exercises", on_delete=fields.CASCADE)
    type = fields.CharEnumField(ExerciseTypeEnum)
    intensity = fields.CharEnumField(IntensityLevelEnum)
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "exercises"
```

---

### 🔢 **sets** (Séries)

Armazena as séries/repetições de cada exercício.

#### Estrutura da Tabela:

| Campo               | Tipo      | Descrição                                    | Constraints                  |
|---------------------|-----------|----------------------------------------------|------------------------------|
| `id`                | UUID      | Identificador único da série                 | PRIMARY KEY                  |
| `exercise_id`       | UUID      | Referência ao exercício                      | FOREIGN KEY, CASCADE DELETE  |
| `reps`              | INTEGER   | Número de repetições                         | NULLABLE                     |
| `weight`            | FLOAT     | Peso utilizado (em kg)                       | NULLABLE                     |
| `duration`          | INTEGER   | Duração (em segundos)                        | NULLABLE                     |
| `calories_burned`   | FLOAT     | Calorias queimadas na série                  | DEFAULT 0.0                  |
| `created_at`        | DATETIME  | Data de criação da série                     | AUTO_NOW_ADD                 |

#### Relacionamentos:
- **N:1** com `exercises` - Várias séries pertencem a um exercício

#### Observações:
- Para exercícios de força: use `reps` e `weight`
- Para exercícios de cardio: use `duration`
- Campos são nullable para flexibilidade
- Pelo menos um campo deve ser preenchido

#### Índices:
- INDEX em `exercise_id` (foreign key)

#### Modelo Tortoise ORM:

```python
from tortoise import Model, fields

class Set(Model):
    id = fields.UUIDField(pk=True)
    exercise = fields.ForeignKeyField("models.Exercisse", related_name="sets", on_delete=fields.CASCADE)
    reps = fields.IntField(null=True)
    weight = fields.FloatField(null=True)
    duration = fields.IntField(null=True)
    calories_burned = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "sets"
```

---

### 🍽️ **caloric_intakes** (Ingestão Calórica)

Registra a ingestão calórica e macronutrientes do usuário.

#### Estrutura da Tabela:

| Campo         | Tipo      | Descrição                              | Constraints                  |
|---------------|-----------|----------------------------------------|------------------------------|
| `id`          | UUID      | Identificador único do registro        | PRIMARY KEY                  |
| `user_id`     | UUID      | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE  |
| `calories`    | FLOAT     | Total de calorias ingeridas            | NOT NULL                     |
| `protein_g`   | FLOAT     | Proteínas em gramas                    | NULLABLE                     |
| `carbs_g`     | FLOAT     | Carboidratos em gramas                 | NULLABLE                     |
| `fat_g`       | FLOAT     | Gorduras em gramas                     | NULLABLE                     |
| `created_at`  | DATETIME  | Data e hora do registro                | AUTO_NOW_ADD                 |

#### Relacionamentos:
- **N:1** com `users` - Vários registros pertencem a um usuário

#### Regras de Validação:
- Calorias são obrigatórias
- Macronutrientes são opcionais
- Valores devem ser positivos

#### Índices:
- INDEX em `user_id` (foreign key)
- INDEX em `created_at` para agregação por período

---

## 🔗 Relacionamentos e Integridade

### Estratégia de CASCADE DELETE:

Todos os relacionamentos usam `ON DELETE CASCADE`, garantindo que:

```
Deletar USER → Deleta automaticamente:
  ├─ body_assessments (todas as avaliações)
  ├─ workouts (todos os treinos)
  │  └─ exercises (todos os exercícios dos treinos)
  │     └─ sets (todas as séries dos exercícios)
  └─ caloric_intakes (todos os registros de alimentação)
```

### Grafo de Dependências:

```
USER
├── BODY_ASSESSMENTS
├── WORKOUTS
│   └── EXERCISES
│       └── SETS
└── CALORIC_INTAKES
```

---

## ⚡ Índices e Performance

### Índices Criados:

| Tabela             | Campo        | Tipo    | Propósito                          |
|--------------------|--------------|---------|------------------------------------|
| `users`            | `email`      | UNIQUE  | Login rápido, garantir unicidade   |
| `body_assessments` | `user_id`    | INDEX   | Listar avaliações por usuário      |
| `body_assessments` | `created_at` | INDEX   | Ordenação temporal                 |
| `workouts`         | `user_id`    | INDEX   | Listar treinos por usuário         |
| `workouts`         | `start_time` | INDEX   | Filtros por data                   |
| `exercises`        | `workout_id` | INDEX   | Carregar exercícios de um treino   |
| `sets`             | `exercise_id`| INDEX   | Carregar séries de um exercício    |
| `caloric_intakes`  | `user_id`    | INDEX   | Listar registros por usuário       |
| `caloric_intakes`  | `created_at` | INDEX   | Agregação por período              |

### Otimizações Implementadas:

1. **UUIDs como PKs**: Melhor distribuição em índices
2. **Soft Delete**: Campo `activates_at` permite desativação sem perda de dados
3. **Timestamps Automáticos**: `auto_now_add` e `auto_now`
4. **Eager Loading**: Use `prefetch_related()` para evitar N+1 queries

---

## 📊 Enumerações (Enums)

### GenderEnum (user.py)
```python
class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
```

### ActivityLevelEnum (user.py)
```python
class ActivityLevelEnum(str, Enum):
    SEDENTARY = "sedentary"           # Pouco ou nenhum exercício
    LIGHT = "light"                   # Exercício leve 1-3 dias/semana
    MODERATE = "moderate"             # Exercício moderado 3-5 dias/semana
    HIGH = "high"                     # Exercício intenso 6-7 dias/semana
    EXTRA_ACTIVE = "extra_active"     # Exercício muito intenso
    ATHLETE = "athlete"               # Treino diário intenso
```

### RoleEnum (user.py)
```python
class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
```

### TrainingTypeEnum (workout.py)
```python
class TrainingTypeEnum(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    HIIT = "hiit"
    FUNCTIONAL = "functional"
    OTHER = "other"
```

### ExerciseTypeEnum (exercise.py)
```python
class ExerciseTypeEnum(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
```

### IntensityLevelEnum (exercise.py)
```python
class IntensityLevelEnum(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
```

---

## 📜 Regras de Negócio

### Validações de Usuário:
- ✅ Email deve ser único no sistema
- ✅ Senha deve ter no mínimo 8 caracteres
- ✅ Data de nascimento deve indicar idade mínima de 13 anos
- ✅ Altura e peso devem ser valores positivos

### Validações de Avaliação Corporal:
- ✅ Peso e altura são obrigatórios
- ✅ Valores devem ser positivos
- ✅ BFP requer medidas mínimas (cintura, pescoço, altura)
- ✅ Para mulheres, quadril é obrigatório no cálculo Navy

### Validações de Treino:
- ✅ Nome do treino é obrigatório
- ✅ `end_time` deve ser posterior a `start_time`
- ✅ Usuário só pode criar/editar seus próprios treinos

### Validações de Série:
- ✅ Pelo menos um campo deve ser preenchido (reps, weight ou duration)
- ✅ Valores devem ser positivos

### Constraints do Banco:
- 🔒 `ON DELETE CASCADE`: Garante integridade referencial
- 🔒 `UNIQUE`: Previne duplicação de emails
- 🔒 `NOT NULL`: Campos obrigatórios garantidos
- 🔒 `DEFAULT`: Valores padrão para campos opcionais

---

## 🔄 Migrações

O projeto usa **Aerich** para gerenciar migrações do Tortoise ORM.

### Arquivos de Migração:

```
migrations/
└── models/
    ├── 0_20260105000058_init.py      # Migração inicial
    └── 1_20260109160251_update.py     # Atualização de esquema
```

### Comandos Úteis:

```bash
# Inicializar Aerich
aerich init -t src.core.database.db_config.TORTOISE_ORM

# Criar nova migração
aerich migrate --name "descricao_da_mudanca"

# Aplicar migrações
aerich upgrade

# Reverter última migração
aerich downgrade

# Ver histórico
aerich history
```

### Configuração (pyproject.toml):

```toml
[tool.aerich]
tortoise_orm = "src.core.database.db_config.TORTOISE_ORM"
location = "./migrations"
src_folder = "./src"
```

---

## 🔄 Fluxos de Dados

### 1. Criação de Treino Completo

```
1. Usuário cria um Workout
   ├─ POST /workout/
   ├─ Workout é salvo com user_id, start_time
   │
2. Sistema cria Exercises dentro do Workout
   ├─ POST /exercise/
   ├─ Cada Exercise é salvo com workout_id
   │
3. Sistema cria Sets para cada Exercise
   ├─ POST /set/
   ├─ Cada Set é salvo com exercise_id
   │
4. Sistema calcula calorias (em desenvolvimento)
   ├─ Calorias dos Sets → agregadas no Exercise
   ├─ Calorias dos Exercises → agregadas no Workout
   │
5. Workout finalizado com total_calories_burned calculado
   ├─ PUT /workout/{id}
   ├─ end_time registrado
```

### 2. Avaliação Corporal

```
1. Usuário registra medidas corporais
   ├─ POST /body-assessment/
   ├─ Envia: weight_kg, height_cm, circunferências, dobras
   │
2. Sistema calcula métricas automaticamente
   ├─ BMI = peso / (altura²)
   ├─ BFP = Método Navy (se houver medidas)
   ├─ BMR = Fórmula Mifflin-St Jeor
   ├─ TDEE = BMR × fator de atividade
   ├─ Massa Magra e Gorda
   │
3. Avaliação salva com todos os cálculos
   ├─ body_assessment criado com user_id
   ├─ Campos calculados preenchidos automaticamente
```

### 3. Registro de Alimentação

```
1. Usuário registra refeição
   ├─ POST /caloric-intake/
   ├─ Envia: calories, protein_g, carbs_g, fat_g
   │
2. Sistema armazena registro
   ├─ caloric_intake criado com user_id
   ├─ Timestamp automático (created_at)
   │
3. Registro disponível para análise
   ├─ GET /caloric-intake/
   ├─ Agregação por período
```

### 4. Consulta de Histórico

```
Query de Evolução de Peso:
SELECT created_at, weight_kg
FROM body_assessments
WHERE user_id = ?
ORDER BY created_at ASC

Query de Calorias por Dia:
SELECT DATE(created_at) as day, SUM(calories) as total
FROM caloric_intakes
WHERE user_id = ?
GROUP BY DATE(created_at)
ORDER BY day DESC
```

---

## 🛠️ Tecnologias

- **Banco de Dados**: PostgreSQL (prod/dev)
- **ORM**: Tortoise ORM 0.25.3
- **Migrações**: Aerich 0.9.2
- **Driver**: asyncpg (assíncrono)
- **Conexão**: Connection pooling automático

---

## 📝 Notas Técnicas

### Conexão Assíncrona:

```python
from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='postgres://user:pass@host:port/dbname',
        modules={'models': ['src.types.models']}
    )
    await Tortoise.generate_schemas()
```

### Queries Otimizadas:

```python
# ❌ N+1 Problem
workouts = await Workout.filter(user_id=user_id).all()
for workout in workouts:
    exercises = await workout.exercises.all()  # N queries

# ✅ Prefetch Related
workouts = await Workout.filter(user_id=user_id).prefetch_related("exercises").all()
```

### Transações:

```python
from tortoise.transactions import in_transaction

async with in_transaction() as conn:
    user = await User.create(...)
    await BodyAssessment.create(user=user, ...)
```

---

## 🔍 Referências

- [Tortoise ORM Documentation](https://tortoise.github.io/)
- [Aerich Documentation](https://github.com/tortoise/aerich)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Contato:** yhann.mendes@poraygua.com.br  
**Versão do Documento:** 1.0.0
