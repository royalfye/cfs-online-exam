Readme

```
# 🎓 CFS Online Exam System

Sistema de provas online para o Curso de Formação de Sargentos (CFS), com:

- Interface web para resolução de provas (Streamlit)
- API backend com FastAPI + SQLAlchemy + PostgreSQL
- Autenticação com JWT (OAuth2 password flow)
- Controle de acesso baseado em roles (`aluno`, `instrutor`, `admin`)

---

## 📋 Funcionalidades

### Backend (FastAPI)

- ✅ Cadastro de usuários (`POST /users/`)
- ✅ Login com JWT via OAuth2 password flow (`POST /auth/token`)
- ✅ Hash de senha com Argon2
- ✅ Dependência `get_current_user` para obter usuário autenticado
- ✅ Helpers de autorização por role:
  - `require_role(*roles: UserRole)`
  - `AdminUser`
  - `AdminOrInstrutorUser`
- ✅ Endpoints protegidos por papel:
  - `GET /users/me` – dados do usuário autenticado
  - `PATCH /users/me` – atualização parcial pelo próprio usuário
  - `GET /users/{user_id}` – acesso restrito a `admin` ou `instrutor`
  - `DELETE /users/{user_id}` – apenas `admin`

### Frontend (Streamlit)

- ✅ Interface interativa para resolver provas
- ✅ Integração com API FastAPI para login (JWT)
- ✅ Exibição de dados do usuário logado (nome, username, role)
- ✅ Verificação instantânea de respostas
- ✅ Histórico de anos disponíveis (2014–ano atual)
- ✅ Navegação por páginas (10 questões por página)
- ✅ Feedback visual de acertos/erros
- ✅ Barra de progresso respondido
- ✅ Reset de respostas
- ✅ Logout que limpa sessão e token

---

## 📂 Estrutura de diretórios

```text
cfs-online-exam
├── .gitignore
├── README.md
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   └── exams_with_answers.csv
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── main.py              # Instancia o FastAPI e registra as rotas
│   │   └── routes
│   │       ├── __init__.py
│   │       ├── auth.py          # /auth/token (login)
│   │       └── users.py         # /users/... (CRUD, /me, etc.)
│   ├── db
│   │   ├── __init__.py
│   │   ├── database.py          # engine, SessionLocal, Base
│   │   └── models.py            # Modelo User
│   ├── online_exam.py           # Interface Streamlit (frontend)
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── roles.py             # Enum UserRole
│   │   ├── token.py             # Schemas de Token
│   │   └── user.py              # Schemas de usuário (create/read/update)
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py              # Dependências de auth/roles para FastAPI
│   │   ├── exam_service.py      # Carregamento e lógica de provas (CSV)
│   │   ├── security.py          # Hash de senha e JWT
│   │   └── user_service.py      # Lógica de persistência de usuários
│   ├── test_db.py
│   └── test_user_service.py
├── tree.py
└── tree.txt
```

---

## 🗄️ Estrutura do PostgreSQL

```text
Servidor PostgreSQL (localhost:5432)
└── Databases
    ├── postgres          # banco padrão
    └── cfs_online_exam   # banco da aplicação
        └── Schemas
            └── public
                ├── Tables
                │   └── users
                │       ├── id           (SERIAL, PK, sequence users_id_seq)
                │       ├── username     (VARCHAR(50), NOT NULL, UNIQUE)
                │       ├── email        (VARCHAR(120), NOT NULL, UNIQUE)
                │       ├── password_hash(VARCHAR(255), NOT NULL)
                │       ├── full_name    (VARCHAR(120), NOT NULL)
                │       ├── birth_date   (DATE, NOT NULL)
                │       ├── role         (VARCHAR(20), NOT NULL)
                │       ├── rank         (VARCHAR(50), NULL)
                │       └── created_at   (TIMESTAMPTZ, DEFAULT NOW())
                └── Sequences
                    └── users_id_seq     # sequência usada pelo campo id
```

### 📂 Roles do PostgreSQL

```text
Roles (usuários do PostgreSQL)
├── postgres       # superusuário
└── cfs_user       # usuário da aplicação
    ├── CONNECT em cfs_online_exam
    ├── USAGE em schema public
    ├── SELECT/INSERT/UPDATE/DELETE em tabelas do schema public
    └── USAGE/SELECT em sequências do schema public (users_id_seq, etc.)
```

---

## ⚙️ Configuração básica

### Variáveis de ambiente (opcional, mas recomendado)

Por padrão, o projeto usa no `src/db/database.py`:

```python
DATABASE_URL = "postgresql+psycopg2://cfs_user:123456%40@localhost:5432/cfs_online_exam"
```

Em produção/desenvolvimento mais avançado, recomenda-se usar variável de ambiente:

```bash
# Exemplo de DATABASE_URL
export DATABASE_URL="postgresql+psycopg2://cfs_user:SENHA@localhost:5432/cfs_online_exam"
```

No `config/settings.py`, também há configurações de JWT:

```python
SECRET_KEY = "sua-chave-secreta-super-segura"  # em produção, usar env var
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/cfs-online-exam.git
cd cfs-online-exam
```

### 2. (Opcional) Crie e ative um ambiente virtual

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux / macOS:
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco PostgreSQL

1. Crie o banco (se ainda não existir):

```sql
CREATE DATABASE cfs_online_exam;
CREATE USER cfs_user WITH PASSWORD 'sua_senha_aqui';
GRANT CONNECT ON DATABASE cfs_online_exam TO cfs_user;

\c cfs_online_exam;
GRANT USAGE ON SCHEMA public TO cfs_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO cfs_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO cfs_user;
```

2. Ajuste a `DATABASE_URL` em `src/db/database.py` ou via variável de ambiente, se necessário.

3. Ao iniciar a API FastAPI, as tabelas serão criadas automaticamente pela linha:

```python
Base.metadata.create_all(bind=engine)
```

em `src/api/main.py` (para algo mais robusto, use Alembic no futuro).

---

## ▶️ 5. Inicie o backend (FastAPI)

Na raiz do projeto:

```bash
uvicorn src.api.main:app --reload
```

A API ficará disponível em:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `GET http://localhost:8000/health`

---

## 👤 6. Crie um usuário de teste

Use o Swagger em `http://localhost:8000/docs` ou um cliente HTTP para chamar:

`POST /users/` com body JSON, por exemplo:

```json
{
  "email": "aluno@teste.com",
  "username": "aluno1",
  "full_name": "Aluno Teste",
  "birth_date": "2000-01-01",
  "role": "aluno",
  "rank": null,
  "password": "senha12345"
}
```

---

## 🖥️ 7. Inicie o frontend (Streamlit)

### Forma recomendada

Rodar o Streamlit a partir da raiz do projeto:

```bash
python -m streamlit run src/online_exam.py
```

> Caso tenha problemas com `ModuleNotFoundError: No module named 'src'`, verifique se está rodando a partir da raiz do projeto e usando o comando acima. Alternativamente, ajuste o `PYTHONPATH` ou os imports conforme explicado nos comentários do código.

---

## 🔐 Login (versão atual)

Na versão atual, o **login do Streamlit está integrado à API FastAPI**:

- O Streamlit chama `POST /auth/token` enviando `username` e `password`.
- Em caso de sucesso:
  - O `access_token` (JWT) é armazenado em sessão.
  - O app chama `GET /users/me` para obter os dados do usuário.
  - O usuário é redirecionado para a tela de prova.

Para logar na interface Streamlit, use as credenciais de um usuário que você tenha criado via `POST /users/`.

Exemplo (do passo anterior):

- Usuário: `aluno1`
- Senha: `senha12345`

Após o login:

- A interface exibe nome, username e role do usuário.
- O token JWT fica disponível para futuras integrações com endpoints protegidos.

---
