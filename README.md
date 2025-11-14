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
│   ├── online_exam.py
│   └── services
│       ├── __init__.py
│       └── exam_service.py
├── tree.py
└── tree.txt
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