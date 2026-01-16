# 📚 Documentação KiloCal Backend

> Documentação completa e organizada do backend da aplicação KiloCal

---

## 📂 Estrutura da Documentação

### 📖 Documentos Principais

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **[README_DOCUMENTATION.md](./README_DOCUMENTATION.md)** | 📚 Índice geral e guia de navegação | Comece aqui para entender a estrutura |
| **[DATABASE_COMPLETE_DOCUMENTATION.md](./DATABASE_COMPLETE_DOCUMENTATION.md)** | 🗄️ Documentação completa do banco de dados | Estrutura de tabelas, relacionamentos, migrações |
| **[SERVICES_COMPLETE_DOCUMENTATION.md](./SERVICES_COMPLETE_DOCUMENTATION.md)** | ⚙️ Documentação completa dos serviços | Lógica de negócio, cálculos, validações |
| **[ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md)** | 🚀 Documentação completa das rotas da API | Endpoints, autenticação, exemplos de uso |
| **[API_ROUTES_QUICK_REFERENCE.md](./API_ROUTES_QUICK_REFERENCE.md)** | ⚡ Referência rápida das rotas | Consulta rápida de endpoints |

### 📐 Documentos Complementares

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| **CALCULATIONS_REFERENCE.md** | `server/docs/` | Fórmulas e cálculos matemáticos (IMC, BFP, BMR, TDEE) |

---

## 🚀 Quick Start

### Para Desenvolvedores Backend:

1. Leia: [README_DOCUMENTATION.md](./README_DOCUMENTATION.md) - Visão geral
2. Estude: [DATABASE_COMPLETE_DOCUMENTATION.md](./DATABASE_COMPLETE_DOCUMENTATION.md) - Estrutura de dados
3. Entenda: [SERVICES_COMPLETE_DOCUMENTATION.md](./SERVICES_COMPLETE_DOCUMENTATION.md) - Lógica de negócio
4. Implemente: [ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md) - API

### Para Desenvolvedores Frontend/Mobile:

1. Comece: [API_ROUTES_QUICK_REFERENCE.md](./API_ROUTES_QUICK_REFERENCE.md) - Referência rápida
2. Detalhe: [ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md) - Documentação completa da API

### Para Entender os Cálculos:

1. Consulte: `server/docs/CALCULATIONS_REFERENCE.md` - Todas as fórmulas matemáticas

---

## 📊 Conteúdo por Documento

### 🗄️ Banco de Dados

[DATABASE_COMPLETE_DOCUMENTATION.md](./DATABASE_COMPLETE_DOCUMENTATION.md) contém:

- Diagrama ERD completo
- 6 tabelas detalhadas (users, body_assessments, workouts, exercises, sets, caloric_intakes)
- Relacionamentos e CASCADE DELETE
- Índices e otimizações
- Enumerações completas
- Sistema de migrações (Aerich)
- Modelos Tortoise ORM

### ⚙️ Serviços

[SERVICES_COMPLETE_DOCUMENTATION.md](./SERVICES_COMPLETE_DOCUMENTATION.md) contém:

- UserService - Registro, login, perfil
- BodyAssessmentService - Avaliações corporais e cálculos
- WorkoutService - Gerenciamento de treinos
- ExerciseService - Gerenciamento de exercícios
- SetService - Gerenciamento de séries
- SessionService - Controle de sessões
- Tratamento de erros e validações
- Boas práticas e otimizações

### 🚀 Rotas da API

[ROUTES_COMPLETE_DOCUMENTATION.md](./ROUTES_COMPLETE_DOCUMENTATION.md) contém:

- 13 endpoints documentados
- Sistema de autenticação JWT
- Headers, body, query parameters
- Exemplos cURL completos
- Códigos de resposta HTTP
- Middlewares (CORS e Auth)

[API_ROUTES_QUICK_REFERENCE.md](./API_ROUTES_QUICK_REFERENCE.md) contém:

- Referência rápida de todos os endpoints
- Exemplos práticos prontos para copiar
- Enums e tipos
- Códigos de erro

### 📐 Cálculos

`server/docs/CALCULATIONS_REFERENCE.md` contém:

- Fórmulas matemáticas completas
- IMC (Body Mass Index)
- BFP (Body Fat Percentage) - Método Navy
- BMR (Basal Metabolic Rate) - Mifflin-St Jeor
- TDEE (Total Daily Energy Expenditure)
- Massa Magra e Massa Gorda
- Cálculo de idade

---

## 🔍 Busca Rápida

### Como encontrar...

**...Como autenticar?**
→ [ROUTES_COMPLETE_DOCUMENTATION.md - Autenticação](./ROUTES_COMPLETE_DOCUMENTATION.md#autenticação)

**...Como criar um usuário?**
→ [API_ROUTES_QUICK_REFERENCE.md - Registro](./API_ROUTES_QUICK_REFERENCE.md#registro-de-usuário)

**...Como calcular IMC?**
→ `server/docs/CALCULATIONS_REFERENCE.md`

**...Estrutura do banco?**
→ [DATABASE_COMPLETE_DOCUMENTATION.md - Tabelas](./DATABASE_COMPLETE_DOCUMENTATION.md#tabelas-detalhadas)

**...Como criar uma avaliação corporal?**
→ [SERVICES_COMPLETE_DOCUMENTATION.md - BodyAssessmentService](./SERVICES_COMPLETE_DOCUMENTATION.md#bodyassessmentservice)

**...Lista de todos os endpoints?**
→ [API_ROUTES_QUICK_REFERENCE.md](./API_ROUTES_QUICK_REFERENCE.md)

---

## 🛠️ Stack Tecnológica

- **Python 3.11+**
- **FastAPI 0.128.0**
- **Tortoise ORM 0.25.3**
- **PostgreSQL**
- **JWT (Python-Jose)**
- **Bcrypt (Passlib)**
- **Pydantic 2.12.5**

---

## 📝 Organização dos Arquivos

```
docs/
├── README.md                                # 📄 Este arquivo
├── README_DOCUMENTATION.md                  # 📚 Índice geral detalhado
├── DATABASE_COMPLETE_DOCUMENTATION.md       # 🗄️ Banco de dados completo
├── SERVICES_COMPLETE_DOCUMENTATION.md       # ⚙️ Serviços completos
├── ROUTES_COMPLETE_DOCUMENTATION.md         # 🚀 Rotas completas
└── API_ROUTES_QUICK_REFERENCE.md            # ⚡ Referência rápida

server/docs/
└── CALCULATIONS_REFERENCE.md                # 📐 Fórmulas matemáticas
```

---

## ✅ Status da Documentação

| Documento | Status | Última Atualização |
|-----------|--------|-------------------|
| README_DOCUMENTATION.md | ✅ Completo | 16/01/2026 |
| DATABASE_COMPLETE_DOCUMENTATION.md | ✅ Completo | 16/01/2026 |
| SERVICES_COMPLETE_DOCUMENTATION.md | ✅ Completo | 16/01/2026 |
| ROUTES_COMPLETE_DOCUMENTATION.md | ✅ Completo | 16/01/2026 |
| API_ROUTES_QUICK_REFERENCE.md | ✅ Completo | 16/01/2026 |
| CALCULATIONS_REFERENCE.md | ✅ Completo | Original |

---

## 🤝 Contribuindo

Ao atualizar a documentação:

1. ✅ Mantenha consistência com o código
2. ✅ Adicione exemplos práticos
3. ✅ Atualize a data de modificação
4. ✅ Revise links entre documentos
5. ✅ Teste os exemplos cURL

---

## 🌐 Links Úteis

### Desenvolvimento:
- API: http://localhost:8000/api/v1
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Produção:
- API: https://kilocal-8fy9.onrender.com/api/v1
- Swagger UI: https://kilocal-8fy9.onrender.com/docs
- ReDoc: https://kilocal-8fy9.onrender.com/redoc

---

## 📞 Contato

**Autor:** Yhann Matheus de Dio Miranda Mendes  
**Email:** yhann.mendes@poraygua.com.br  
**GitHub:** [YhannMatheus/KiloCal](https://github.com/YhannMatheus/KiloCal)

---

**Última Atualização:** 16 de Janeiro de 2026  
**Versão da Documentação:** 1.0.0
