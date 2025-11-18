```markdown
# 🎓 CFS Online Exam System

Sistema de provas online para o Curso de Formação de Sargentos (CFS).

## 📋 Funcionalidades

- ✅ Interface interativa para resolver provas
- ✅ Verificação instantânea de respostas
- ✅ Histórico de anos disponíveis (2014-2025)
- ✅ Navegação por páginas (10 questões por página)
- ✅ Feedback visual de acertos/erros
- ✅ Sistema de reset de respostas
- ✅ Tela de login simples (usuário/senha fixos por enquanto)

```

## 📂 Estrutura de diretórios

```text

cfs-online-exam
├── .venv/
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
│   ├── online_exam.py
│   ├── test_db.py
│   ├── test_user_service.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── database.py       # Conexão com PostgreSQL via SQLAlchemy (engine, SessionLocal, Base)
│   │   └── models.py         # Modelo User mapeando a tabela users
│   └── services
│       ├── __init__.py
│       ├── exam_service.py   # Lê CSV de provas
│       └── user_service.py   # Funções create_user, get_user_by_username
├── tree.py
└── tree.txt
```

## 📂 Estrutura do PostgreSQL

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

## 📂 Estrutura lógica do banco em roles

```text

Roles (usuários do PostgreSQL)
├── postgres       # superusuário
└── cfs_user       # usuário da aplicação
    ├── CONNECT em cfs_online_exam
    ├── USAGE em schema public
    ├── SELECT/INSERT/UPDATE/DELETE em tabelas do schema public
    └── USAGE/SELECT em sequências do schema public (users_id_seq, etc.)

```

## 🚀 Como usar

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

### 4. Inicie a aplicação

```bash
streamlit run src/online_exam.py
```

## 🔐 Login

Na versão atual, o login utiliza credenciais fixas apenas para demonstração:

- Usuário: `admin`
- Senha: `1234`

Após o login, o usuário tem acesso à interface de resolução de provas.
```