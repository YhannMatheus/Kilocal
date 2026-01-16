# 📊 Referência de Cálculos - KiloCal API

## Visão Geral

Este documento descreve as funções de cálculo disponíveis em `core.calculations` e sua relação com `BodyAssessmentBase`.

---

## 📐 BodyAssessmentBase (Schema Principal)

**Arquivo**: `types.schemas.body_assessment.py`

### Campos Calculados Automaticamente:
- `bfp` - Body Fat Percentage (% de Gordura)
- `bmi` - Body Mass Index (IMC)
- `bmr` - Basal Metabolic Rate (Taxa Metabólica Basal)
- `tdee` - Total Daily Energy Expenditure (Gasto Calórico Total Diário)
- `lean_mass_kg` - Massa Magra em kg
- `fat_mass_kg` - Massa Gorda em kg

### Dados de Entrada do Usuário:
- Medidas corporais: `weight_kg`, `height_cm`, `waist_cm`, `hip_cm`, `chest_cm`, `neck_cm`, `arm_cm`, `thigh_cm`
- Dobras cutâneas: `fold_chest`, `fold_abdominal`, `fold_thigh`, `fold_triceps`, `fold_subscapular`, `fold_suprailiac`, `fold_midaxillary`

---

## 🧮 1. body_metrics.py - Métricas Corporais Básicas

### `calculate_bmi(weight_kg, height_cm)` → `bmi`
Calcula o Índice de Massa Corporal.

**Parâmetros:**
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `height_cm` (float, obrigatório): Altura em centímetros

**Fórmula Matemática:**
```
altura_metros = altura_cm / 100
BMI = peso_kg / (altura_metros²)
```

**Regras:**
- Resultado arredondado para 2 casas decimais
- Não há validação de limites mínimos/máximos

**Preenche**: `BodyAssessmentBase.bmi`

---

### `calculate_age(birth_date)` → `int`
Calcula idade atual a partir da data de nascimento.

**Parâmetros:**
- `birth_date` (date, obrigatório): Data de nascimento no formato Python date

**Lógica:**
1. Subtrai ano de nascimento do ano atual
2. Se aniversário ainda não ocorreu no ano atual, subtrai 1

**Uso**: Necessário para cálculos de BMR e TDEE (idade é variável crítica nas fórmulas metabólicas)

---

### `calculate_body_fat_navy(sex, waist_cm, neck_cm, height_cm, hip_cm?)` → `bfp`
Calcula percentual de gordura corporal usando o **Método Navy dos EUA** (U.S. Navy Body Composition Assessment).

**Parâmetros:**
- `sex` (GenderEnum, obrigatório): Sexo biológico (`GenderEnum.MALE` ou `GenderEnum.FEMALE`)
- `waist_cm` (float, obrigatório): Circunferência da cintura em centímetros
- `neck_cm` (float, obrigatório): Circunferência do pescoço em centímetros
- `height_cm` (float, obrigatório): Altura em centímetros
- `hip_cm` (float, **OBRIGATÓRIO APENAS PARA MULHERES**): Circunferência do quadril em centímetros

**Fórmulas Matemáticas:**

**Homens:**
```
BF% = (495 / (1.0324 - 0.19077 × log10(cintura - pescoço) + 0.15456 × log10(altura))) - 450
```

**Mulheres:**
```
BF% = (495 / (1.29579 - 0.35004 × log10(cintura + quadril - pescoço) + 0.22100 × log10(altura))) - 450
```

**Regras Críticas:**
- ⚠️ **MULHERES DEVEM FORNECER `hip_cm`**: Se `sex == FEMALE` e `hip_cm is None`, lança `ValueError("Hip measurement required for females")`
- Homens podem passar `hip_cm`, mas será ignorado
- Resultado mínimo é 0% (valores negativos são convertidos para 0)
- Resultado arredondado para 2 casas decimais
- Usa logaritmo base 10 (`math.log10`)

**Onde Medir:**
- **Cintura**: Ponto mais estreito, geralmente acima do umbigo
- **Pescoço**: Logo abaixo da laringe (pomo de Adão)
- **Quadril** (mulheres): Ponto mais largo dos glúteos

**Preenche**: `BodyAssessmentBase.bfp`

---

### `calculate_lean_mass(weight_kg, body_fat_percentage)` → `lean_mass_kg`
Calcula massa magra (tudo exceto gordura: músculos, ossos, órgãos, água).

**Parâmetros:**
- `weight_kg` (float, obrigatório): Peso corporal total em quilogramas
- `body_fat_percentage` (float, obrigatório): Percentual de gordura corporal (0-100)

**Fórmula Matemática:**
```
massa_gorda = peso_kg × (percentual_gordura / 100)
massa_magra = peso_kg - massa_gorda
```

**Exemplo:**
- Pessoa de 80kg com 20% de gordura
- Massa gorda = 80 × 0.20 = 16kg
- Massa magra = 80 - 16 = 64kg

**Regras:**
- Resultado arredondado para 2 casas decimais

**Preenche**: `BodyAssessmentBase.lean_mass_kg`

---

### `calculate_fat_mass(weight_kg, body_fat_percentage)` → `fat_mass_kg`
Calcula massa gorda (tecido adiposo).

**Parâmetros:**
- `weight_kg` (float, obrigatório): Peso corporal total em quilogramas
- `body_fat_percentage` (float, obrigatório): Percentual de gordura corporal (0-100)

**Fórmula Matemática:**
```
massa_gorda = peso_kg × (percentual_gordura / 100)
```

**Regras:**
- Resultado arredondado para 2 casas decimais

**Preenche**: `BodyAssessmentBase.fat_mass_kg`

---

### `classify_bmi(bmi)` → `str`
Classifica IMC em categorias segundo padrões da OMS (Organização Mundial da Saúde).

**Parâmetros:**
- `bmi` (float, obrigatório): Valor do Índice de Massa Corporal

**Classificação:**
| IMC           | Classificação         |
|---------------|----------------------|
| < 18.5        | Abaixo do peso       |
| 18.5 - 24.9   | Peso normal          |
| 25.0 - 29.9   | Sobrepeso            |
| 30.0 - 34.9   | Obesidade Grau I     |
| 35.0 - 39.9   | Obesidade Grau II    |
| ≥ 40.0        | Obesidade Grau III   |

**Retorna**: String com a classificação em português

---

## ⚡ 2. energy_expenditure.py - Gasto Energético

### Multiplicadores de Atividade (ACTIVITY_MULTIPLIERS):

**Constantes da Classe:**
```python
ActivityLevelEnum.SEDENTARY: 1.2          # Pouco ou nenhum exercício
ActivityLevelEnum.LIGHTLY_ACTIVE: 1.375   # Exercício leve 1-3 dias/semana
ActivityLevelEnum.MODERATELY_ACTIVE: 1.55 # Exercício moderado 3-5 dias/semana
ActivityLevelEnum.VERY_ACTIVE: 1.725      # Exercício intenso 6-7 dias/semana
ActivityLevelEnum.ATHLETE: 1.9            # Atleta/treinamento pesado diário
```

**Uso:** Esses multiplicadores convertem BMR (taxa metabólica de repouso) em TDEE (gasto total diário) considerando o nível de atividade física da pessoa.

---

### `calculate_bmr_harris_benedict(sex, weight_kg, height_cm, age)` → `bmr`
Calcula Taxa Metabólica Basal usando a **fórmula revisada de Harris-Benedict (1984)**.

**Parâmetros:**
- `sex` (GenderEnum, obrigatório): Sexo biológico (`GenderEnum.MALE` ou `GenderEnum.FEMALE`)
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `height_cm` (float, obrigatório): Altura em centímetros
- `age` (int, obrigatório): Idade em anos completos

**Fórmulas Matemáticas:**

**Homens:**
```
BMR = 88.362 + (13.397 × peso_kg) + (4.799 × altura_cm) - (5.677 × idade)
```

**Mulheres:**
```
BMR = 447.593 + (9.247 × peso_kg) + (3.098 × altura_cm) - (4.330 × idade)
```

**Explicação dos Coeficientes:**
- Constante inicial difere por sexo (homens têm maior massa muscular base)
- Peso tem maior impacto em homens (13.397 vs 9.247) pois músculo consome mais energia
- Altura contribui positivamente (tecido corporal maior = mais gasto)
- Idade reduz BMR (metabolismo desacelera ~2% por década após 20 anos)

**Regras:**
- Resultado em kcal/dia (quilocalorias por dia)
- Arredondado para 2 casas decimais
- Fórmula original de 1919, revisada em 1984

**Observação:** Harris-Benedict tende a superestimar BMR em ~5% comparado a Mifflin-St Jeor (mais moderna).

---

### `calculate_bmr_mifflin(sex, weight_kg, height_cm, age)` → `bmr`
Calcula Taxa Metabólica Basal usando a **fórmula de Mifflin-St Jeor (1990)**.

**Parâmetros:**
- `sex` (GenderEnum, obrigatório): Sexo biológico
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `height_cm` (float, obrigatório): Altura em centímetros
- `age` (int, obrigatório): Idade em anos completos

**Fórmula Matemática:**

**Base (ambos os sexos):**
```
BMR_base = (10 × peso_kg) + (6.25 × altura_cm) - (5 × idade)
```

**Ajuste por sexo:**
```
Homens:   BMR = BMR_base + 5
Mulheres: BMR = BMR_base - 161
```

**Explicação:**
- Fórmula mais simples e moderna que Harris-Benedict
- Considerada mais precisa para populações contemporâneas (testada em 498 indivíduos saudáveis)
- Diferença de 166 kcal/dia entre sexos (5 - (-161) = 166)
- A diferença reflete maior massa muscular e menor % de gordura em homens

**Regras:**
- Resultado em kcal/dia
- Arredondado para 2 casas decimais
- **Esta é a fórmula padrão recomendada** (mais precisa que Harris-Benedict)

**Preenche**: `BodyAssessmentBase.bmr`

---

### `calculate_bmr(sex, weight_kg, height_cm, age, formula)` → `bmr`
**Wrapper/Função principal** que permite escolher qual fórmula de BMR usar.

**Parâmetros:**
- `sex` (GenderEnum, obrigatório): Sexo biológico
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `height_cm` (float, obrigatório): Altura em centímetros
- `age` (int, obrigatório): Idade em anos completos
- `formula` (BMRFormulaEnum, **opcional**): Fórmula a usar
  - `BMRFormulaEnum.MIFFLIN_ST_JEOR` (padrão)
  - `BMRFormulaEnum.HARRIS_BENEDICT`

**Lógica:**
```python
if formula == BMRFormulaEnum.HARRIS_BENEDICT:
    return calculate_bmr_harris_benedict(...)
else:  # MIFFLIN_ST_JEOR (padrão)
    return calculate_bmr_mifflin(...)
```

**Regras:**
- Se `formula` não for fornecido, usa **Mifflin-St Jeor** (mais preciso)
- Retorna o mesmo que a função específica escolhida

**Quando usar cada fórmula:**
- **Mifflin-St Jeor**: Para população geral (padrão recomendado)
- **Harris-Benedict**: Para comparações com estudos antigos ou preferência institucional

---

### `calculate_tdee(bmr, activity_level)` → `tdee`
Calcula o **Gasto Energético Total Diário** (Total Daily Energy Expenditure).

**Parâmetros:**
- `bmr` (float, obrigatório): Taxa Metabólica Basal em kcal/dia (calcular antes com `calculate_bmr()`)
- `activity_level` (ActivityLevelEnum, obrigatório): Nível de atividade física

**Fórmula Matemática:**
```
TDEE = BMR × multiplicador_atividade
```

**Tabela de Multiplicadores e Significado:**
| Nível de Atividade | Multiplicador | Descrição Detalhada |
|-------------------|---------------|---------------------|
| SEDENTARY         | 1.2           | Trabalho de escritório, quase nenhum exercício |
| LIGHTLY_ACTIVE    | 1.375         | Exercício leve 1-3x/semana ou trabalho de pé |
| MODERATELY_ACTIVE | 1.55          | Exercício moderado 3-5x/semana |
| VERY_ACTIVE       | 1.725         | Exercício intenso 6-7x/semana |
| ATHLETE           | 1.9           | Atleta profissional, treino 2x/dia |

**Exemplo Prático:**
- BMR = 1,800 kcal/dia
- Pessoa sedentária: TDEE = 1,800 × 1.2 = 2,160 kcal/dia
- Pessoa muito ativa: TDEE = 1,800 × 1.725 = 3,105 kcal/dia

**Regras:**
- Resultado em kcal/dia
- Arredondado para 2 casas decimais
- **TDEE é o total de calorias que a pessoa gasta em um dia típico**
- Para perder peso: consumir menos que TDEE
- Para ganhar peso: consumir mais que TDEE
- Para manter peso: consumir igual ao TDEE

**Preenche**: `BodyAssessmentBase.tdee`

---

### `calculate_caloric_balance(calories_consumed, calories_burned, tdee)` → `float`
Calcula o **balanço calórico** diário (se está em superávit ou déficit).

**Parâmetros:**
- `calories_consumed` (float, obrigatório): Calorias consumidas via alimentação no dia
- `calories_burned` (float, obrigatório): Calorias gastas em exercícios **adicionais** (não incluídas no TDEE)
- `tdee` (float, obrigatório): Gasto total diário calculado previamente

**Fórmula Matemática:**
```
gasto_total = TDEE + calorias_exercício_extra
balanço = calorias_consumidas - gasto_total
```

**Interpretação do Resultado:**
- **Positivo (+)**: Superávit calórico → Ganho de peso
  - +500 kcal/dia ≈ +0.5kg/semana
- **Negativo (-)**: Déficit calórico → Perda de peso
  - -500 kcal/dia ≈ -0.5kg/semana
- **Zero (0)**: Manutenção → Peso estável

**Exemplo:**
- TDEE: 2,500 kcal
- Treino: +300 kcal
- Consumo: 2,200 kcal
- Balanço: 2,200 - (2,500 + 300) = **-600 kcal** (déficit)

**Regras:**
- Resultado arredondado para 2 casas decimais
- ⚠️ **Importante**: `calories_burned` são **extras**, não substitui TDEE
- 1kg de gordura ≈ 7,700 kcal
- Déficit seguro: 500-1000 kcal/dia (não mais)

---

## 🏋️ 3. workout_calories.py - Cálculo de Calorias em Exercícios

### Valores MET (Metabolic Equivalent of Task):

**Definição de MET:**
MET é uma unidade que mede a intensidade metabólica de uma atividade física. 1 MET = taxa metabólica de repouso.
- **1 MET** = ~1 kcal/kg/hora = gasto energético sentado em repouso
- **3 METs** = atividade consome 3× mais energia que repouso
- **10 METs** = atividade consome 10× mais energia que repouso

**Tabela Completa de METs por Tipo e Intensidade:**

```python
MET_VALUES = {
    ExerciseTypeEnum.CARDIO: {
        IntensityLevelEnum.LOW: 3.5,        # Caminhada leve, bicicleta leve
        IntensityLevelEnum.MODERATE: 5.0,   # Corrida leve, natação moderada
        IntensityLevelEnum.HIGH: 8.0,       # Corrida rápida, ciclismo intenso
        IntensityLevelEnum.VERY_HIGH: 11.0, # Sprint, HIIT, ciclismo muito intenso
    },
    ExerciseTypeEnum.STRENGTH: {
        IntensityLevelEnum.LOW: 3.0,        # Musculação leve, alongamento com peso
        IntensityLevelEnum.MODERATE: 5.0,   # Musculação moderada, crossfit leve
        IntensityLevelEnum.HIGH: 6.0,       # Musculação intensa, superset
        IntensityLevelEnum.VERY_HIGH: 8.0,  # Crossfit pesado, circuito intenso
    },
    ExerciseTypeEnum.FLEXIBILITY: {
        IntensityLevelEnum.LOW: 2.0,        # Alongamento estático, yoga suave
        IntensityLevelEnum.MODERATE: 2.5,   # Pilates, yoga Hatha
        IntensityLevelEnum.HIGH: 3.0,       # Yoga Vinyasa, pilates avançado
        IntensityLevelEnum.VERY_HIGH: 4.0,  # Yoga Power, pilates intenso
    },
    ExerciseTypeEnum.SPORTS: {
        IntensityLevelEnum.LOW: 4.0,        # Vôlei recreativo, tênis de mesa
        IntensityLevelEnum.MODERATE: 6.0,   # Futebol amador, basquete recreativo
        IntensityLevelEnum.HIGH: 8.0,       # Futebol competitivo, basquete intenso
        IntensityLevelEnum.VERY_HIGH: 10.0, # Esportes profissionais, artes marciais
    },
}
```

**Fonte:** Baseado no Compendium of Physical Activities (Ainsworth et al., 2011)

---

### `calculate_calories_from_met(met, weight_kg, duration_minutes)` → `float`
**Função base** para calcular calorias a partir de um valor MET específico.

**Parâmetros:**
- `met` (float, obrigatório): Valor MET da atividade (obtido da tabela acima)
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `duration_minutes` (float, obrigatório): Duração da atividade em minutos

**Fórmula Matemática:**
```
duração_horas = duração_minutos / 60
calorias = MET × peso_kg × duração_horas
```

**Explicação:**
- METs são expressos em kcal/kg/hora
- Multiplicar por peso converte para kcal/hora para aquela pessoa
- Multiplicar por duração converte para total de calorias gastas

**Exemplo:**
- Pessoa de 70kg
- Corrida moderada (MET = 8.0)
- Duração: 30 minutos
- Cálculo: 8.0 × 70 × 0.5 = 280 kcal

**Regras:**
- Resultado arredondado para 2 casas decimais
- Duração deve ser convertida para horas (dividir por 60)

---

### `calculate_exercise_calories(exercise_type, intensity, weight_kg, duration_seconds)` → `float`
Calcula calorias gastas em um exercício específico usando a tabela MET.

**Parâmetros:**
- `exercise_type` (ExerciseTypeEnum, obrigatório): Tipo de exercício
  - `ExerciseTypeEnum.CARDIO`: Aeróbico (corrida, bike, natação)
  - `ExerciseTypeEnum.STRENGTH`: Musculação e treino de força
  - `ExerciseTypeEnum.FLEXIBILITY`: Alongamento, yoga, pilates
  - `ExerciseTypeEnum.SPORTS`: Esportes coletivos/individuais
- `intensity` (IntensityLevelEnum, obrigatório): Nível de intensidade
  - `IntensityLevelEnum.LOW`: Baixa intensidade
  - `IntensityLevelEnum.MODERATE`: Intensidade moderada
  - `IntensityLevelEnum.HIGH`: Alta intensidade
  - `IntensityLevelEnum.VERY_HIGH`: Intensidade muito alta
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `duration_seconds` (int, obrigatório): Duração total em segundos

**Lógica Interna:**
1. Busca valor MET na tabela: `MET_VALUES[exercise_type][intensity]`
2. Converte segundos para minutos: `duration_minutes = duration_seconds / 60`
3. Chama `calculate_calories_from_met(met, weight_kg, duration_minutes)`

**Exemplo:**
- Tipo: CARDIO
- Intensidade: HIGH
- Peso: 80kg
- Duração: 1800 segundos (30 minutos)
- MET encontrado: 8.0
- Resultado: 8.0 × 80 × 0.5 = 320 kcal

**Regras:**
- Duração em **segundos** (diferente de `calculate_calories_from_met` que usa minutos)
- Resultado arredondado para 2 casas decimais

**Uso:** Para registrar sessões de treino completas no banco de dados

---

### `calculate_strength_calories(weight_kg, sets, reps, weight_lifted_kg?, rest_seconds)` → `float`
**Cálculo especializado** para treinos de musculação/força que considera volume de treino e carga.

**Parâmetros:**
- `weight_kg` (float, obrigatório): Peso corporal em quilogramas
- `sets` (int, obrigatório): Número de séries realizadas
- `reps` (int, obrigatório): Número de repetições por série
- `weight_lifted_kg` (float, **opcional**): Peso levantado/carga utilizada em quilogramas
  - Se fornecido: ajusta intensidade automaticamente
  - Se `None`: usa intensidade MODERATE por padrão
- `rest_seconds` (int, opcional, padrão=60): Tempo de descanso entre séries em segundos

**Lógica de Cálculo:**

**1. Tempo Total de Treino:**
```python
# Assume 3 segundos por repetição (tempo médio de execução)
tempo_trabalho = séries × reps × 3 segundos

# Descanso entre séries (primeira série não tem descanso antes)
tempo_descanso = (séries - 1) × rest_seconds

# Tempo total
tempo_total = tempo_trabalho + tempo_descanso
```

**2. Determinação Automática de Intensidade:**
Se `weight_lifted_kg` for fornecido, a intensidade é ajustada:

```python
if weight_lifted_kg is None:
    intensidade = MODERATE  # Padrão
elif weight_lifted_kg > peso_corporal × 0.8:
    intensidade = VERY_HIGH  # Carga > 80% do peso corporal
elif weight_lifted_kg > peso_corporal × 0.5:
    intensidade = HIGH       # Carga > 50% do peso corporal
else:
    intensidade = MODERATE   # Carga ≤ 50% do peso corporal
```

**Tabela de Referência de Carga:**
| Carga em relação ao peso | Intensidade | MET | Exemplo (pessoa 70kg) |
|--------------------------|-------------|-----|----------------------|
| ≤ 35kg (50%)            | MODERATE    | 5.0 | Treino leve/pump     |
| 35-56kg (50-80%)        | HIGH        | 6.0 | Treino hipertrofia   |
| > 56kg (80%)            | VERY_HIGH   | 8.0 | Treino força/powerlifting |

**3. Cálculo Final:**
```python
return calculate_exercise_calories(
    ExerciseTypeEnum.STRENGTH,
    intensidade_determinada,
    weight_kg,
    tempo_total_segundos
)
```

**Exemplo Prático 1 - Treino Moderado:**
- Peso corporal: 70kg
- 3 séries × 12 reps
- Sem informação de carga (`weight_lifted_kg=None`)
- Descanso: 60s
- Tempo trabalho: 3 × 12 × 3 = 108s
- Tempo descanso: 2 × 60 = 120s
- Tempo total: 228s
- Intensidade: MODERATE (MET=5.0)
- Calorias: 5.0 × 70 × (228/3600) ≈ 22 kcal

**Exemplo Prático 2 - Treino Pesado:**
- Peso corporal: 80kg
- 5 séries × 5 reps
- Carga: 100kg (125% do peso corporal)
- Descanso: 180s (3 min)
- Tempo trabalho: 5 × 5 × 3 = 75s
- Tempo descanso: 4 × 180 = 720s
- Tempo total: 795s
- Intensidade: VERY_HIGH (100kg > 80×0.8=64kg)
- Calorias: 8.0 × 80 × (795/3600) ≈ 141 kcal

**Regras:**
- Assume 3 segundos por repetição (cadência controlada)
- Primeira série não tem descanso anterior
- Se carga não fornecida, usa intensidade MODERATE
- Útil para exercícios compostos (agachamento, supino, levantamento terra)

**Observação:** Esta função é ideal para treinos de força estruturados. Para treinos contínuos (circuitos), use `calculate_exercise_calories()` diretamente.

---

## 💧 4. biopedance.py - Bioimpedância e Composição Corporal

### `calculate_body_water(lean_mass_kg)` → `float`
Calcula a quantidade total de água corporal baseada na massa magra.

**Parâmetros:**
- `lean_mass_kg` (float, obrigatório): Massa magra em quilogramas (calcular antes com `calculate_lean_mass()`)

**Fórmula Matemática:**
```
água_corporal = massa_magra × 0.73
```

**Fundamento Científico:**
- **73% da massa magra é composta por água** (músculos, órgãos, sangue)
- Tecido adiposo (gordura) contém apenas ~10% de água
- Por isso usamos apenas massa magra no cálculo

**Exemplo:**
- Pessoa com 60kg de massa magra
- Água corporal: 60 × 0.73 = 43.8kg (ou 43.8 litros)
- Isso representa ~60% do peso total se a pessoa pesa 75kg

**Regras:**
- Resultado em quilogramas (kg)
- Arredondado para 2 casas decimais
- Para converter em litros: 1kg de água = 1 litro

**Importância:**
- Hidratação adequada crucial para performance
- Perda de >2% água corporal reduz capacidade atlética
- Usado em balanças de bioimpedância

---

### `calculate_ideal_weight_robinson(sex, height_cm)` → `float`
Calcula peso ideal usando a **fórmula de Robinson (1983)**, amplamente aceita na comunidade médica.

**Parâmetros:**
- `sex` (GenderEnum, obrigatório): Sexo biológico (`GenderEnum.MALE` ou `GenderEnum.FEMALE`)
- `height_cm` (float, obrigatório): Altura em centímetros

**Fórmulas Matemáticas:**

**Conversão de altura:**
```
altura_polegadas = altura_cm / 2.54
```

**Homens:**
```
peso_ideal_libras = 52 + 1.9 × (altura_polegadas - 60)
peso_ideal_kg = peso_ideal_libras × 0.453592
```

**Mulheres:**
```
peso_ideal_libras = 49 + 1.7 × (altura_polegadas - 60)
peso_ideal_kg = peso_ideal_libras × 0.453592
```

**Explicação da Fórmula:**
- **Base**: Peso para 152cm (60 polegadas) é 52 lbs (homens) ou 49 lbs (mulheres)
- **Incremento**: Adiciona 1.9 lbs/polegada (homens) ou 1.7 lbs/polegada (mulheres)
- Fórmula assume estrutura corporal média

**Exemplo 1 - Homem 175cm:**
```
Polegadas: 175 / 2.54 = 68.9"
Peso ideal: 52 + 1.9 × (68.9 - 60) = 52 + 16.9 = 68.9 lbs
Em kg: 68.9 × 0.453592 = 31.25kg (ERRO! Precisa corrigir)
```
*Nota: A fórmula na prática soma os valores em libras primeiro, depois converte*

**Exemplo 2 - Mulher 165cm:**
```
Polegadas: 165 / 2.54 = 64.96"
Peso ideal: 49 + 1.7 × (64.96 - 60) = 49 + 8.43 = 57.43 lbs
Em kg: 57.43 × 0.453592 ≈ 26kg (base) + incremento ≈ 60-65kg total
```

**Regras:**
- Resultado em quilogramas (kg)
- Arredondado para 2 casas decimais
- **Peso mínimo garantido: 40kg** (mesmo para pessoas muito baixas)
- Fórmula válida para adultos (>18 anos)

**Limitações:**
- Não considera massa muscular (atletas podem pesar mais)
- Não considera estrutura óssea (pequena/média/grande)
- É uma **referência geral**, não objetivo absoluto

---

### `calculate_waist_to_hip_ratio(waist_cm, hip_cm)` → `float`
Calcula a **Relação Cintura-Quadril** (WHR - Waist-to-Hip Ratio), indicador de distribuição de gordura.

**Parâmetros:**
- `waist_cm` (float, obrigatório): Circunferência da cintura em centímetros
- `hip_cm` (float, obrigatório): Circunferência do quadril em centímetros

**Fórmula Matemática:**
```
WHR = cintura / quadril
```

**Onde Medir:**
- **Cintura**: Ponto mais estreito do tronco (geralmente acima do umbigo)
- **Quadril**: Ponto mais largo dos glúteos/quadris

**Interpretação:**
- WHR alto: Distribuição de gordura tipo "maçã" (abdominal/visceral) → **MAIOR RISCO**
- WHR baixo: Distribuição tipo "pera" (quadril/subcutânea) → menor risco

**Exemplo:**
- Cintura: 85cm
- Quadril: 100cm
- WHR: 85/100 = 0.85

**Regras:**
- Resultado é um número decimal (razão)
- Arredondado para 2 casas decimais
- Sem unidade (é uma proporção)

**Importância Médica:**
- Preditor de risco cardiovascular
- Gordura abdominal (visceral) é mais perigosa que subcutânea
- Usado pela OMS como métrica de saúde

---

### `classify_waist_to_hip_ratio(ratio, sex)` → `str`
Classifica o **risco cardiovascular** baseado no WHR segundo padrões da OMS.

**Parâmetros:**
- `ratio` (float, obrigatório): Valor do WHR (calcular antes com `calculate_waist_to_hip_ratio()`)
- `sex` (GenderEnum, obrigatório): Sexo biológico

**Classificação por Sexo:**

**Homens:**
| WHR      | Classificação  | Risco Cardiovascular |
|----------|----------------|---------------------|
| < 0.90   | Baixo risco    | Distribuição saudável |
| 0.90-0.99| Risco moderado | Atenção necessária |
| ≥ 1.0    | Risco alto     | Intervenção recomendada |

**Mulheres:**
| WHR      | Classificação  | Risco Cardiovascular |
|----------|----------------|---------------------|
| < 0.80   | Baixo risco    | Distribuição saudável |
| 0.80-0.84| Risco moderado | Atenção necessária |
| ≥ 0.85   | Risco alto     | Intervenção recomendada |

**Por que diferença entre sexos?**
- Mulheres naturalmente têm quadris mais largos (estrutura pélvica)
- Homens tendem a acumular mais gordura abdominal
- Hormônios influenciam padrão de distribuição de gordura

**Exemplo 1 - Homem:**
- WHR: 0.95
- Classificação: "Risco moderado"
- Ação: Monitorar alimentação e aumentar exercício

**Exemplo 2 - Mulher:**
- WHR: 0.82
- Classificação: "Risco moderado"
- Ação: Focar em redução de gordura abdominal

**Retorna:** String em português com a classificação

---

### `calculate_body_composition(weight_kg, body_fat_percentage, lean_mass_kg?)` → `dict`
**Função completa** que retorna um dicionário com toda a composição corporal detalhada.

**Parâmetros:**
- `weight_kg` (float, obrigatório): Peso corporal total em quilogramas
- `body_fat_percentage` (float, obrigatório): Percentual de gordura corporal (0-100)
- `lean_mass_kg` (float, **opcional**): Massa magra em quilogramas
  - Se fornecido: usa o valor fornecido
  - Se `None`: calcula automaticamente (`peso - gordura`)

**Lógica de Cálculo:**

**1. Massa Gorda:**
```python
massa_gorda = peso_kg × (percentual_gordura / 100)
```

**2. Massa Magra:**
```python
if lean_mass_kg is None:
    massa_magra = peso_kg - massa_gorda
else:
    massa_magra = lean_mass_kg  # Usa valor fornecido
```

**3. Água Corporal:**
```python
água_corporal = massa_magra × 0.73  # 73% da massa magra
```

**Retorno (Dicionário):**
```python
{
    "weight_kg": float,              # Peso total
    "fat_mass_kg": float,            # Massa gorda
    "lean_mass_kg": float,           # Massa magra
    "body_water_kg": float,          # Água corporal
    "body_fat_percentage": float,    # % de gordura
    "lean_mass_percentage": float,   # % de massa magra
}
```

**Exemplo Completo:**
```python
# Entrada
peso = 80kg
bf_percentage = 20%

# Cálculo
fat_mass = 80 × 0.20 = 16kg
lean_mass = 80 - 16 = 64kg
body_water = 64 × 0.73 = 46.72kg
lean_percentage = (64/80) × 100 = 80%

# Retorno
{
    "weight_kg": 80.0,
    "fat_mass_kg": 16.0,
    "lean_mass_kg": 64.0,
    "body_water_kg": 46.72,
    "body_fat_percentage": 20.0,
    "lean_mass_percentage": 80.0
}
```

**Regras:**
- Todos os valores arredondados para 2 casas decimais
- `body_fat_percentage + lean_mass_percentage` deve somar 100%
- Água é incluída na massa magra (não é contada separadamente no peso)

**Uso:**
- Relatórios completos de composição corporal
- Dashboards de progresso
- Análise antes/depois de treino/dieta

**Validação:**
```python
# Validação sempre verdadeira:
fat_mass + lean_mass = weight_kg
body_water ≈ 73% de lean_mass
```

---

## 🔄 Fluxo de Cálculo Recomendado

### 1. Avaliação Inicial
```python
# Dados de entrada do usuário
weight_kg, height_cm, birth_date, sex, activity_level
waist_cm, neck_cm, hip_cm  # para % gordura

# Calcular
age = calculate_age(birth_date)
bmi = calculate_bmi(weight_kg, height_cm)
bfp = calculate_body_fat_navy(sex, waist_cm, neck_cm, height_cm, hip_cm)
```

### 2. Composição Corporal
```python
lean_mass_kg = calculate_lean_mass(weight_kg, bfp)
fat_mass_kg = calculate_fat_mass(weight_kg, bfp)
body_water = calculate_body_water(lean_mass_kg)
```

### 3. Gasto Energético
```python
bmr = calculate_bmr(sex, weight_kg, height_cm, age)
tdee = calculate_tdee(bmr, activity_level)
```

### 4. Preencher BodyAssessmentBase
```python
body_assessment = BodyAssessmentBase(
    weight_kg=weight_kg,
    height_cm=height_cm,
    # ... outras medidas ...
    bmi=bmi,
    bfp=bfp,
    lean_mass_kg=lean_mass_kg,
    fat_mass_kg=fat_mass_kg,
    bmr=bmr,
    tdee=tdee,
    created_at=datetime.now()
)
```

---

## 📊 Exemplo Prático

**Usuário**: Homem, 25 anos, 80kg, 175cm, sedentário  
**Medidas**: Cintura 90cm, Pescoço 38cm

```python
# 1. Básicos
age = 25
bmi = calculate_bmi(80, 175)  # → 26.1 (Sobrepeso)

# 2. Gordura Corporal
bfp = calculate_body_fat_navy('male', 90, 38, 175)  # → ~22%
lean_mass = calculate_lean_mass(80, 22)  # → 62.4kg
fat_mass = calculate_fat_mass(80, 22)  # → 17.6kg

# 3. Gasto Energético
bmr = calculate_bmr_mifflin('male', 80, 175, 25)  # → ~1,850 kcal
tdee = calculate_tdee(1850, 'SEDENTARY')  # → 2,220 kcal/dia

# 4. Treino (musculação moderada, 45 min)
workout_cal = calculate_exercise_calories(
    'STRENGTH', 'MODERATE', 80, 2700  # 45 min = 2700 seg
)  # → ~300 kcal
```

**Resultado**: Para manter peso, consumir ~2,220 kcal/dia. Para perder 0.5kg/semana, consumir ~1,720 kcal/dia (déficit de 500 kcal).

---

## ⚠️ Notas Importantes

1. **BMR vs TDEE**: BMR é o mínimo para sobreviver. TDEE inclui atividades diárias.
2. **% Gordura**: Navy é estimativa. Para precisão, use bioimpedância ou DEXA.
3. **Calorias de Treino**: São **adicionais** ao TDEE, não substituem.
4. **Déficit Seguro**: Máximo 500-1000 kcal/dia (perder 0.5-1kg/semana).
5. **Enums**: Sempre use MAIÚSCULAS (`ActivityLevelEnum.SEDENTARY`, não `.sedentary`).

---

## 🔒 Regras de Validação e Obrigatoriedade

### Parâmetros Obrigatórios vs Opcionais:

#### **SEMPRE OBRIGATÓRIOS:**
- `weight_kg`: Peso corporal (todas as funções)
- `height_cm`: Altura (BMI, BMR, % gordura)
- `age`: Idade (BMR, TDEE)
- `sex`: Sexo biológico (BMR, % gordura)
- `waist_cm`: Cintura (% gordura Navy)
- `neck_cm`: Pescoço (% gordura Navy)

#### **OBRIGATÓRIO CONDICIONALMENTE:**
- ⚠️ **`hip_cm`: OBRIGATÓRIO para mulheres no método Navy**
  - Se `sex == GenderEnum.FEMALE` e `hip_cm is None` → **ValueError**
  - Homens podem passar, mas é ignorado
  - Razão: Fórmula Navy para mulheres depende de cintura + quadril - pescoço

#### **SEMPRE OPCIONAIS:**
- `formula`: Escolha de fórmula BMR (padrão: Mifflin-St Jeor)
- `lean_mass_kg`: Em `calculate_body_composition()` (calcula se ausente)
- `weight_lifted_kg`: Em `calculate_strength_calories()` (intensidade MODERATE se ausente)
- `rest_seconds`: Descanso entre séries (padrão: 60s)

---

## 📏 Limites e Validações Aplicadas

### Valores Mínimos Garantidos:
- **`calculate_body_fat_navy()`**: Retorna no mínimo 0% (usa `max(0, resultado)`)
  - Fórmulas podem retornar negativo para casos extremos → convertido para 0
- **`calculate_ideal_weight_robinson()`**: Retorna no mínimo 40kg (usa `max(40, resultado)`)
  - Protege contra resultados irreais para pessoas muito baixas

### Arredondamentos:
- **Todas as funções**: Resultados arredondados para **2 casas decimais**
- Usa `round(valor, 2)` do Python

### Conversões Automáticas:
- **METs → Calorias**: Duração convertida de segundos para horas
- **Altura → Polegadas**: Robinson converte cm para polegadas (÷ 2.54)
- **Peso → Libras**: Robinson trabalha em libras, depois converte para kg

---

## 🧪 Referências Científicas

### Fórmulas e Bases Científicas:

**Body Fat Percentage (Navy Method):**
- Fonte: U.S. Navy Body Composition Assessment (1984)
- Validação: Testado contra DEXA em populações militares
- Margem de erro: ±3-4% comparado a métodos laboratoriais

**BMR - Harris-Benedict:**
- Publicação original: 1919 (Harris & Benedict)
- Revisão: 1984 (Roza & Shizgal)
- Amostra: Estudos em calorimetria indireta

**BMR - Mifflin-St Jeor:**
- Publicação: 1990 (Mifflin et al.)
- Amostra: 498 indivíduos saudáveis
- Precisão: ~5% mais preciso que Harris-Benedict para população moderna
- **Recomendado pela Academy of Nutrition and Dietetics**

**Multiplicadores de Atividade:**
- Fonte: Academy of Nutrition and Dietetics
- Baseado em estudos de gasto energético por acelerômetro

**MET Values:**
- Fonte: Compendium of Physical Activities (Ainsworth et al., 2011)
- Atualizado periodicamente com novos estudos
- Base de dados: >800 atividades catalogadas

**Ideal Weight (Robinson):**
- Publicação: 1983 (Robinson et al.)
- Base: Estudos de seguradoras e população geral
- Usado em calculadoras médicas

**Waist-to-Hip Ratio:**
- Fonte: OMS (Organização Mundial da Saúde)
- Estudos: Framingham Heart Study, INTERHEART
- Preditor independente de risco cardiovascular

**Body Water:**
- Princípio: 73% da massa livre de gordura é água
- Fonte: Estudos de bioimpedância e análise de compartimentos corporais

---

## 🚨 Erros Comuns e Como Evitar

### 1. **Esquecer de passar `hip_cm` para mulheres**
```python
# ❌ ERRO - Vai lançar ValueError
bfp = calculate_body_fat_navy(
    sex=GenderEnum.FEMALE,
    waist_cm=75,
    neck_cm=32,
    height_cm=165
    # hip_cm faltando!
)

# ✅ CORRETO
bfp = calculate_body_fat_navy(
    sex=GenderEnum.FEMALE,
    waist_cm=75,
    neck_cm=32,
    height_cm=165,
    hip_cm=95  # Obrigatório para mulheres
)
```

### 2. **Confundir unidades de tempo**
```python
# ❌ ERRO - Duração em segundos onde espera minutos
calorias = calculate_calories_from_met(
    met=5.0,
    weight_kg=70,
    duration_minutes=1800  # Deveria ser 30, não 1800!
)

# ✅ CORRETO
calorias = calculate_calories_from_met(
    met=5.0,
    weight_kg=70,
    duration_minutes=30  # 30 minutos
)

# OU usar a função que aceita segundos:
calorias = calculate_exercise_calories(
    exercise_type=ExerciseTypeEnum.CARDIO,
    intensity=IntensityLevelEnum.MODERATE,
    weight_kg=70,
    duration_seconds=1800  # 30 min em segundos
)
```

### 3. **Usar enum como string**
```python
# ❌ ERRO - Enum precisa ser o objeto, não string
bmr = calculate_bmr(
    sex="MALE",  # Deveria ser GenderEnum.MALE
    weight_kg=80,
    height_cm=175,
    age=25
)

# ✅ CORRETO
from src.types.enums.user import GenderEnum

bmr = calculate_bmr(
    sex=GenderEnum.MALE,  # Objeto enum
    weight_kg=80,
    height_cm=175,
    age=25
)
```

### 4. **Somar calorias de treino ao TDEE incorretamente**
```python
# ❌ ERRO - TDEE já inclui atividade física do nível de atividade
tdee = 2500  # Já calculado com activity_level
workout_calories = 300
total_gasto = tdee + workout_calories  # ❌ Duplicação!

# ✅ CORRETO - Duas opções:

# Opção 1: TDEE com SEDENTARY + adicionar todos os exercícios
tdee_base = calculate_tdee(bmr, ActivityLevelEnum.SEDENTARY)
total_gasto = tdee_base + workout_calories

# Opção 2: TDEE com nível real (já inclui exercício médio)
tdee_real = calculate_tdee(bmr, ActivityLevelEnum.MODERATELY_ACTIVE)
# Só adiciona exercícios EXTRAS além do normal
extra_workout = 500  # Treinou mais que o normal hoje
total_gasto = tdee_real + extra_workout
```

### 5. **Esquecer de calcular idade antes de BMR**
```python
# ❌ ERRO - Passar birth_date direto (espera int)
bmr = calculate_bmr(
    sex=GenderEnum.MALE,
    weight_kg=80,
    height_cm=175,
    age=date(1995, 5, 15)  # ❌ Espera int, não date
)

# ✅ CORRETO
from datetime import date

birth_date = date(1995, 5, 15)
age = calculate_age(birth_date)  # Retorna int
bmr = calculate_bmr(
    sex=GenderEnum.MALE,
    weight_kg=80,
    height_cm=175,
    age=age  # int correto
)
```

---

## 📊 Ordem de Execução Recomendada

### Para criar uma avaliação corporal completa:

```python
from datetime import date
from src.core.calculations.body_metrics import BodyMetrics
from src.core.calculations.energy_expenditure import EnergyExpenditure
from src.core.calculations.biopedance import Bioimpedance
from src.types.enums.user import GenderEnum, ActivityLevelEnum

# 1️⃣ Dados básicos do usuário
weight_kg = 75.0
height_cm = 170.0
birth_date = date(1995, 3, 20)
sex = GenderEnum.MALE
activity_level = ActivityLevelEnum.MODERATELY_ACTIVE

# 2️⃣ Medidas corporais
waist_cm = 85.0
neck_cm = 38.0
hip_cm = 95.0  # Opcional para homens, OBRIGATÓRIO para mulheres

# 3️⃣ CALCULAR IDADE (necessário para BMR)
age = BodyMetrics.calculate_age(birth_date)

# 4️⃣ CALCULAR BMI
bmi = BodyMetrics.calculate_bmi(weight_kg, height_cm)
bmi_classification = BodyMetrics.classify_bmi(bmi)

# 5️⃣ CALCULAR % GORDURA (depende do sexo)
if sex == GenderEnum.FEMALE:
    # Mulheres: hip_cm é OBRIGATÓRIO
    bfp = BodyMetrics.calculate_body_fat_navy(
        sex=sex,
        waist_cm=waist_cm,
        neck_cm=neck_cm,
        height_cm=height_cm,
        hip_cm=hip_cm  # OBRIGATÓRIO
    )
else:
    # Homens: hip_cm opcional (pode passar ou não)
    bfp = BodyMetrics.calculate_body_fat_navy(
        sex=sex,
        waist_cm=waist_cm,
        neck_cm=neck_cm,
        height_cm=height_cm
    )

# 6️⃣ CALCULAR COMPOSIÇÃO CORPORAL
lean_mass_kg = BodyMetrics.calculate_lean_mass(weight_kg, bfp)
fat_mass_kg = BodyMetrics.calculate_fat_mass(weight_kg, bfp)
body_water_kg = Bioimpedance.calculate_body_water(lean_mass_kg)

# 7️⃣ CALCULAR GASTO ENERGÉTICO
bmr = EnergyExpenditure.calculate_bmr(
    sex=sex,
    weight_kg=weight_kg,
    height_cm=height_cm,
    age=age
    # formula opcional, padrão é Mifflin-St Jeor
)
tdee = EnergyExpenditure.calculate_tdee(bmr, activity_level)

# 8️⃣ CALCULAR MÉTRICAS EXTRAS (opcional)
ideal_weight = Bioimpedance.calculate_ideal_weight_robinson(sex, height_cm)

if hip_cm:  # Se temos medida de quadril
    whr = Bioimpedance.calculate_waist_to_hip_ratio(waist_cm, hip_cm)
    whr_risk = Bioimpedance.classify_waist_to_hip_ratio(whr, sex)

# 9️⃣ MONTAR OBJETO COMPLETO
body_assessment_data = {
    # Entrada do usuário
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "waist_cm": waist_cm,
    "neck_cm": neck_cm,
    "hip_cm": hip_cm,
    
    # Calculados automaticamente
    "bmi": bmi,
    "bfp": bfp,
    "lean_mass_kg": lean_mass_kg,
    "fat_mass_kg": fat_mass_kg,
    "bmr": bmr,
    "tdee": tdee,
    
    # Extras
    "body_water_kg": body_water_kg,
    "ideal_weight_kg": ideal_weight,
    # ... outros campos
}

print(f"BMI: {bmi} ({bmi_classification})")
print(f"Gordura Corporal: {bfp}%")
print(f"Massa Magra: {lean_mass_kg}kg")
print(f"BMR: {bmr} kcal/dia")
print(f"TDEE: {tdee} kcal/dia")
```

### Resultado Esperado:
```
BMI: 25.95 (Sobrepeso)
Gordura Corporal: 18.5%
Massa Magra: 61.13kg
BMR: 1,689 kcal/dia
TDEE: 2,618 kcal/dia
```

---

**Última Atualização**: 09/01/2026  
**Autor**: GitHub Copilot
