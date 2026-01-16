# 📚 Índice Geral da Documentação - KiloCal Backend

> **Versão:** 1.0.0  
> **Última Atualização:** 16 de Janeiro de 2026

---

## 🎯 Visão Geral

Esta documentação completa está organizada em três pilares fundamentais do backend KiloCal:

1. **🗄️ Banco de Dados** - Estrutura, relacionamentos e persistência
2. **⚙️ Serviços** - Lógica de negócio e orquestração
3. **🚀 Rotas** - API REST e endpoints HTTP

---

## 📑 Estrutura da Documentação

```
docs/
├── README_DOCUMENTATION.md               # 📚 Este arquivo (índice geral)
├── DATABASE_COMPLETE_DOCUMENTATION.md    # 🗄️ Banco de Dados (completo)
├── SERVICES_COMPLETE_DOCUMENTATION.md    # ⚙️ Serviços (completo)
├── ROUTES_COMPLETE_DOCUMENTATION.md      # 🚀 Rotas (completo)
└── API_ROUTES_QUICK_REFERENCE.md         # ⚡ Referência Rápida de Rotas
```

---

## 🗄️ 1. Documentação do Banco de Dados

**Arquivo:** [DATABASE_COMPLETE_DOCUMENTATION.md](./DATABASE_COMPLETE_DOCUMENTATION.md)

### O que você encontrará:

- ✅ **Diagrama ERD Completo** - Visualização de todas as tabelas e relacionamentos
- ✅ **Estrutura Detalhada das Tabelas**
  - `users` - Usuários do sistema
  - `body_assessments` - Avaliações corporais
  - `workouts` - Treinos
  - `exercises` - Exercícios
  - `sets` - Séries
  - `caloric_intakes` - Ingestão calórica
- ✅ **Relacionamentos e Integridade Referencial**
- ✅ **Índices e Otimizações de Performance**
- ✅ **Enumerações (Enums)** - Todos os valores possíveis
- ✅ **Regras de Negócio e Validações**
- ✅ **Sistema de Migrações** - Como gerenciar mudanças no schema
- ✅ **Fluxos de Dados** - Como os dados transitam entre tabelas
- ✅ **Modelos Tortoise ORM** - Código Python dos modelos

### Quando usar:

- 📌 Criar novas migrações
- 📌 Entender relacionamentos entre tabelas
- 📌 Otimizar queries
- 📌 Adicionar novas tabelas ou campos
- 📌 Compreender constraints e validações

---

## ⚙️ 2. Documentação dos Serviços

**Arquivo:** [SERVICES_COMPLETE_DOCUMENTATION.md](./SERVICES_COMPLETE_DOCUMENTATION.md)

### O que você encontrará:

- ✅ **Arquitetura de Serviços** - Service Layer Pattern
- ✅ **UserService** - Gerenciamento de usuários e autenticação
  - `create_user()` - Registro de novos usuários
  - `get_user()` - Login e autenticação
  - `get_by_id()` - Buscar usuário por ID
  - `get_user_profile()` - Perfil completo
- ✅ **BodyAssessmentService** - Avaliações corporais
  - `create_body_assessment()` - Criar avaliação com cálculos automáticos
  - `get_body_assessment()` - Buscar avaliação específica
  - `get_all_body_assessment_for_user_id()` - Listar todas
  - Métodos de gráficos: `bmi_for_date()`, `bfp_for_date()`, etc.
- ✅ **WorkoutService** - Gerenciamento de treinos
- ✅ **ExerciseService** - Gerenciamento de exercícios
- ✅ **SetService** - Gerenciamento de séries
- ✅ **SessionService** - Gerenciamento de sessões
- ✅ **Tratamento de Erros** - Padrões e boas práticas
- ✅ **Validações** - Regras de negócio
- ✅ **Exemplos de Código** - Como usar cada serviço

### Quando usar:

- 📌 Implementar nova lógica de negócio
- 📌 Entender cálculos automáticos (IMC, BFP, TDEE)
- 📌 Adicionar validações
- 📌 Orquestrar operações complexas
- 📌 Otimizar performance com async/await

---

## 🚀 3. Documentação das Rotas

**Arquivo Principal:** [ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md)  
**Referência Rápida:** [API_ROUTES_QUICK_REFERENCE.md](./API_ROUTES_QUICK_REFERENCE.md) ⚡

### O que você encontrará:

- ✅ **Visão Geral da API REST** - Estrutura e padrões
- ✅ **Sistema de Autenticação JWT**
  - Como funciona o fluxo de autenticação
  - Estrutura do token
  - Middleware de autenticação
- ✅ **Rotas de Usuário** (`/user`)
  - `POST /user/register` - Registro
  - `POST /user/login` - Login
  - `GET /user/profile` - Perfil
- ✅ **Rotas de Avaliação Corporal** (`/body-assessment`)
  - `POST /body-assessment/` - Criar avaliação
  - `GET /body-assessment/` - Listar todas
  - `GET /body-assessment/{id}` - Buscar específica
  - `GET /body-assessment/graph/{user_id}/{type}` - Gráficos
- ✅ **Rotas de Treino** (`/workout`)
  - `POST /workout/` - Criar treino
  - `GET /workout/{userid}` - Listar treinos
  - `GET /workout/detail/{workoutid}` - Detalhes
  - `PUT /workout/{workoutid}` - Atualizar
  - `GET /workout/days/{userid}` - Dias de treino
- ✅ **Códigos HTTP** - Todos os códigos de resposta
- ✅ **Tratamento de Erros** - Formato e exemplos
- ✅ **Exemplos cURL** - Como fazer requisições
- ✅ **Middlewares** - CORS e Autenticação

### Quando usar:

- 📌 Integrar frontend com backend
- 📌 Testar endpoints manualmente
- 📌 Criar documentação de API
- 📌 Debugar requisições HTTP
- 📌 Entender autenticação e permissões

---

## 🔄 Fluxo de Dados Completo

### Exemplo: Criar Avaliação Corporal

```
┌────────────────────────────────────────────────────────────┐
│  1. CLIENTE (Frontend/Mobile)                              │
│  POST /body-assessment/                                    │
│  Headers: Authorization: Bearer {token}                    │
│  Body: { weight_kg: 75, height_cm: 175, ... }            │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  2. MIDDLEWARE DE AUTENTICAÇÃO                             │
│  - Valida token JWT                                        │
│  - Extrai user_id do token                                 │
│  - Disponibiliza para a rota                               │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  3. ROTA (body_assessment.py)                              │
│  - Recebe requisição                                       │
│  - Valida schema Pydantic                                  │
│  - Busca dados do usuário                                  │
│  - Chama serviço                                           │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  4. SERVIÇO (BodyAssessmentService)                        │
│  - Calcula idade do usuário                                │
│  - Calcula IMC                                             │
│  - Calcula % de gordura (método Navy)                      │
│  - Calcula BMR (Mifflin-St Jeor)                          │
│  - Calcula TDEE                                            │
│  - Calcula massa magra e gorda                             │
│  - Persiste no banco via Model                             │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  5. MODEL (BodyAssessment - Tortoise ORM)                  │
│  - Cria registro no banco                                  │
│  - Valida constraints                                      │
│  - Retorna objeto salvo                                    │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  6. BANCO DE DADOS (PostgreSQL)                            │
│  INSERT INTO body_assessments (...)                        │
│  VALUES (...)                                              │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  7. RESPOSTA (JSON)                                        │
│  {                                                         │
│    "id": "uuid",                                           │
│    "bmi": 24.5,                                            │
│    "bfp": 15.2,                                            │
│    "bmr": 1750,                                            │
│    "tdee": 2712,                                           │
│    ...                                                     │
│  }                                                         │
└────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológica

### Backend:
- **Python 3.11+**
- **FastAPI 0.128.0** - Framework web
- **Tortoise ORM 0.25.3** - ORM assíncrono
- **PostgreSQL** - Banco de dados
- **Uvicorn 0.40.0** - Servidor ASGI

### Autenticação:
- **Python-Jose 3.5.0** - JWT
- **Passlib 1.7.4** - Hash de senhas
- **Bcrypt 4.2.1** - Algoritmo de hash

### Validação:
- **Pydantic 2.12.5** - Validação de dados
- **Email-Validator 2.3.0** - Validação de emails

---

## 📖 Como Navegar na Documentação

### 1. Para Desenvolvedores Backend:

**Ordem recomendada:**
1. **Banco de Dados** - Entenda a estrutura de dados
2. **Serviços** - Compreenda a lógica de negócio
3. **Rotas** - Veja como expor funcionalidades via HTTP

### 2. Para Desenvolvedores Frontend:

**Ordem recomendada:**
1. **Rotas** - Comece pelos endpoints disponíveis
2. **Serviços** - Entenda o que acontece internamente (opcional)
3. **Banco de Dados** - Para queries complexas (opcional)

### 3. Para DevOps:

**Foco em:**
- Sistema de Migrações (Banco de Dados)
- Variáveis de Ambiente (Rotas)
- Performance e Índices (Banco de Dados)

### 4. Para QA/Testes:

**Foco em:**
- Exemplos de Requisições (Rotas)
- Validações e Regras de Negócio (Serviços)
- Tratamento de Erros (Rotas e Serviços)

---

## 🔍 Busca Rápida

### Precisa entender como funciona...

**...Autenticação?**
→ [Rotas - Autenticação](./ROUTES_COMPLETE_DOCUMENTATION.md#autenticação)

**...Cálculo de IMC?**
→ [Serviços - BodyAssessmentService](./SERVICES_COMPLETE_DOCUMENTATION.md#bodyassessmentservice)

**...Relacionamento entre tabelas?**
→ [Banco de Dados - Relacionamentos](./DATABASE_COMPLETE_DOCUMENTATION.md#relacionamentos-e-integridade)

**...Criar um novo endpoint?**
→ [Rotas - Estrutura](./ROUTES_COMPLETE_DOCUMENTATION.md#estrutura-de-rotas)

**...Adicionar nova validação?**
→ [Serviços - Validações](./SERVICES_COMPLETE_DOCUMENTATION.md#validações)

**...Criar migração?**
→ [Banco de Dados - Migrações](./DATABASE_COMPLETE_DOCUMENTATION.md#migrações)

---

## 🎯 Padrões e Convenções

### Nomenclatura:

- **Tabelas**: snake_case (users, body_assessments)
- **Classes**: PascalCase (UserService, BodyAssessment)
- **Métodos**: snake_case (create_user, get_by_id)
- **Variáveis**: snake_case (user_id, access_token)
- **Enums**: UPPER_CASE (MALE, SEDENTARY)

### Estrutura de Arquivos:

```
server/
├── src/
│   ├── main.py                    # Entry point
│   ├── core/                      # Configurações e utilities
│   │   ├── auth/                  # Autenticação
│   │   ├── calculations/          # Cálculos matemáticos
│   │   ├── database/              # Configuração do DB
│   │   └── middlewares/           # Middlewares customizados
│   ├── routes/                    # Endpoints da API
│   ├── services/                  # Lógica de negócio
│   └── types/                     # Tipos e modelos
│       ├── models/                # Models do ORM
│       ├── schemas/               # Schemas Pydantic
│       └── enums/                 # Enumerações
└── docs/                          # Documentação
```

---

## 🚀 Quick Start

### 1. Configurar Ambiente:

```bash
# Clone o repositório
git clone https://github.com/YhannMatheus/KiloCal.git
cd KiloCal/server

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados:

```bash
# Configure .env
cp .env.example .env
# Edite .env com suas credenciais

# Execute migrações
aerich upgrade
```

### 3. Rodar Servidor:

```bash
uvicorn src.main:app --reload
```

### 4. Acessar Documentação Interativa:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📊 Estatísticas da Documentação

- **Total de Páginas**: 3 documentos principais
- **Tabelas Documentadas**: 6 tabelas completas
- **Serviços Documentados**: 6 classes de serviço
- **Endpoints Documentados**: 15+ rotas
- **Exemplos de Código**: 50+ snippets
- **Diagramas**: 5 diagramas visuais

---

## 🤝 Contribuindo

### Como Atualizar a Documentação:

1. **Banco de Dados** - Ao adicionar/modificar tabelas
2. **Serviços** - Ao criar novos serviços ou métodos
3. **Rotas** - Ao adicionar novos endpoints

### Checklist de Atualização:

- [ ] Atualizar diagrama ERD (se aplicável)
- [ ] Documentar novos métodos com exemplos
- [ ] Adicionar testes de exemplo
- [ ] Atualizar este índice se necessário
- [ ] Revisar links entre documentos

---

## 📞 Suporte

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Email:** yhann.mendes@poraygua.com.br  
**GitHub:** [YhannMatheus/KiloCal](https://github.com/YhannMatheus/KiloCal)

---

## 📜 Histórico de Versões

| Versão | Data       | Alterações                                    |
|--------|------------|-----------------------------------------------|
| 1.0.0  | 16/01/2026 | Documentação completa inicial                 |

---

**Última Atualização:** 16 de Janeiro de 2026  
**Status:** ✅ Completo e Atualizado
