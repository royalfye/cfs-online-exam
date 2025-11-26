"""
CFS Online Exam System - Main Application
Streamlit interface integrated with FastAPI backend
"""
import streamlit as st
import pandas as pd
import requests
from datetime import date

from src.services.exam_service import load_exam

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8000"  # Ajuste se a API estiver em outra porta/host

# Page configuration
st.set_page_config(
    page_title="CFS Online Exam",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Página de navegação (home, provas_anteriores, etc.)
if 'current_view' not in st.session_state:
    st.session_state.current_view = "inicio"  # "inicio" ou "provas_anteriores"

# Paginação das provas (usada na tela de Provas Anteriores)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'verified' not in st.session_state:
    st.session_state.verified = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# ============================================================================
# API INTEGRATION FUNCTIONS
# ============================================================================

def api_login(username: str, password: str) -> tuple[str, str]:
    """
    Faz login na API FastAPI usando OAuth2PasswordRequestForm.
    
    Args:
        username: Nome de usuário
        password: Senha do usuário
    
    Returns:
        Tupla (access_token, token_type)
    
    Raises:
        ValueError: Se as credenciais forem inválidas ou houver erro na API
    """
    url = f"{API_BASE_URL}/auth/token"
    data = {
        "username": username,
        "password": password,
    }
    # OAuth2PasswordRequestForm espera application/x-www-form-urlencoded
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        
        if response.status_code != 200:
            # Tenta extrair mensagem amigável da API
            try:
                detail = response.json().get("detail", "Erro ao autenticar.")
            except Exception:
                detail = f"Erro ao autenticar. Status code: {response.status_code}"
            raise ValueError(detail)

        token_data = response.json()
        return token_data["access_token"], token_data.get("token_type", "bearer")
    
    except requests.exceptions.ConnectionError:
        raise ValueError("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except requests.exceptions.Timeout:
        raise ValueError("Tempo de conexão esgotado. Tente novamente.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro na requisição: {str(e)}")


def api_get_current_user(access_token: str) -> dict:
    """
    Consulta /users/me para obter dados do usuário autenticado.
    
    Args:
        access_token: Token JWT de autenticação
    
    Returns:
        Dicionário com dados do usuário (id, username, email, role, etc.)
    
    Raises:
        ValueError: Se o token for inválido ou houver erro na API
    """
    url = f"{API_BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", "Erro ao obter usuário atual.")
            except Exception:
                detail = f"Erro ao obter usuário atual. Status code: {response.status_code}"
            raise ValueError(detail)

        return response.json()
    
    except requests.exceptions.ConnectionError:
        raise ValueError("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except requests.exceptions.Timeout:
        raise ValueError("Tempo de conexão esgotado. Tente novamente.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro na requisição: {str(e)}")


# ============================================================================
# EXAM DISPLAY FUNCTIONS
# ============================================================================

def display_question(question: pd.Series, idx: int):
    """
    Display a question with its alternatives and verification button
    
    Args:
        question: Pandas Series contendo os dados da questão
        idx: Índice da questão
    """
    st.markdown(f"### Questão {question['numero']} - {question.get('disciplina', 'N/A')}")
    st.markdown(f"**{question['enunciado']}**")
    st.markdown("---")
    
    key = f"q_{question['ano']}_{question['numero']}"
    answer_key = str(question.get('gabarito', '')).strip().upper()
    
    # Answer options
    letters = ['A', 'B', 'C', 'D']
    options = []
    for letter in letters:
        col_name = f"alternativa_{letter.lower()}"
        if col_name in question and pd.notna(question[col_name]):
            options.append(f"{letter}) {question[col_name]}")
    
    if not options:
        st.warning("⚠️ Questão sem alternativas disponíveis.")
        return
    
    current_answer = st.session_state.answers.get(key, None)
    answer = st.radio(
        "Selecione sua resposta:",
        options,
        key=f"radio_{key}",
        index=options.index(current_answer) if current_answer in options else None
    )
    
    if answer:
        st.session_state.answers[key] = answer
    
    # Button to verify answer
    if st.button("✅ Verificar Resposta", key=f"verify_{key}"):
        chosen_letter = answer.split(")")[0] if ")" in answer else ""
        if chosen_letter == answer_key:
            st.success(f"🎯 Resposta correta! ({answer_key})")
            st.session_state.verified[key] = True
        else:
            st.error(f"❌ Incorreta. A resposta correta é **{answer_key}**.")
            st.session_state.verified[key] = False

    # If already verified, maintain feedback
    elif key in st.session_state.verified:
        if st.session_state.verified[key]:
            st.success(f"🎯 Resposta correta! ({answer_key})")
        else:
            st.error(f"❌ Incorreta. A resposta correta é **{answer_key}**.")

    st.markdown("---")


# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def show_login_page():
    """
    Exibe a página de login integrada com a API FastAPI
    """
    # Espaço no topo
    st.markdown("<br><br>", unsafe_allow_html=True)

    # TÍTULO CENTRALIZADO
    st.markdown(
        """
        <h1 style='text-align: center;'>🔐 Login - CFS Online Exam</h1>
        <p style='text-align: center;'>Por favor, faça login para acessar as provas.</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # COLUNAS PARA A CAIXA DE LOGIN
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        username = st.text_input("Usuário", key="login_username")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar", type="primary", use_container_width=True):
            if not username or not password:
                st.error("⚠️ Por favor, preencha usuário e senha.")
                return

            with st.spinner("Autenticando..."):
                try:
                    # Faz login na API
                    access_token, token_type = api_login(username, password)
                    
                    # Guarda o token na sessão
                    st.session_state.access_token = access_token

                    # Busca dados do usuário logado
                    current_user = api_get_current_user(access_token)
                    st.session_state.current_user = current_user

                    # Marca como logado
                    st.session_state.logged_in = True

                    st.success(f"✅ Login realizado com sucesso! Bem-vindo(a), {current_user.get('full_name', username)}.")
                    st.rerun()

                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")

        # Link para informações adicionais (opcional)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; font-size: 0.9em;'>"
            "Não tem uma conta? Entre em contato com o administrador."
            "</p>",
            unsafe_allow_html=True
        )

def show_top_menu():
    """
    Mostra o menu de navegação principal após login.
    Controla qual 'view' está ativa: Início ou Provas Anteriores.
    """
    st.markdown("## 📚 CFS Online Exam")

    col1, col2, col3 = st.columns([1, 1, 6])

    with col1:
        if st.button("🏠 Início", use_container_width=True):
            st.session_state.current_view = "inicio"
            # opcional: resetar paginação de provas anteriores quando voltar ao início
            st.session_state.current_page = 0
            st.rerun()

    with col2:
        if st.button("📜 Provas Anteriores", use_container_width=True):
            st.session_state.current_view = "provas_anteriores"
            st.session_state.current_page = 0
            st.rerun()

    # Linha separadora
    st.markdown("---")

def show_home_page():
    """
    Página inicial após login, com 3 cards de geração de questões por disciplina.
    (Por enquanto os botões só exibem mensagem; depois podemos integrar com lógica de geração.)
    """
    current_user = st.session_state.current_user or {}
    username = current_user.get("username", "desconhecido")
    full_name = current_user.get("full_name", username)
    role = current_user.get("role", "aluno")

    # Cabeçalho
    st.markdown(f"**Bem-vindo(a), {full_name}!**")
    st.markdown(f"**Perfil:** {role.upper()}")
    st.markdown("---")

    st.markdown("### Selecione o tipo de simulado que deseja gerar:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📘 Legislação Básica")
        st.markdown("Simulados focados em legislação básica.")
        if st.button("Gerar questões: Legislação Básica", use_container_width=True):
            st.info("Função de geração de questões de Legislação Básica ainda será implementada.")

    with col2:
        st.markdown("#### 📕 Legislação Criminal e Administrativa Disciplinar")
        st.markdown("Simulados focados em legislação criminal e administrativa disciplinar.")
        if st.button("Gerar questões: Legislação Criminal e Administrativa Disciplinar", use_container_width=True):
            st.info("Função de geração de questões de Legislação Criminal e Administrativa Disciplinar ainda será implementada.")

    with col3:
        st.markdown("#### 🛠️ Conhecimentos Profissionais")
        st.markdown("Simulados focados em conhecimentos profissionais.")
        if st.button("Gerar questões: Conhecimentos profissionais", use_container_width=True):
            st.info("Função de geração de questões de Conhecimentos Profissionais ainda será implementada.")

def show_old_exams_page():
    """
    Exibe a página de Provas Anteriores (simulados por ano).
    """
    current_user = st.session_state.current_user or {}
    username = current_user.get("username", "desconhecido")
    full_name = current_user.get("full_name", username)
    role = current_user.get("role", "aluno")
    
    # Header com informações do usuário
    st.markdown("### 📜 Provas Anteriores")
    st.markdown(f"**Usuário:** {full_name} | **Role:** {role.upper()}")
    st.markdown("---")

    # ========================================================================
    # SIDEBAR - User info and logout
    # ========================================================================
    st.sidebar.markdown("### 👤 Usuário")
    st.sidebar.markdown(f"**Nome:** {full_name}")
    st.sidebar.markdown(f"**Username:** {username}")
    st.sidebar.markdown(f"**Role:** {role.upper()}")
    
    if st.sidebar.button("🚪 Sair", use_container_width=True):
        # Limpa toda a sessão
        st.session_state.logged_in = False
        st.session_state.access_token = None
        st.session_state.current_user = None
        st.session_state.answers = {}
        st.session_state.verified = {}
        st.session_state.current_page = 0
        st.session_state.current_view = "inicio"
        st.success("Logout realizado com sucesso!")
        st.rerun()

    st.sidebar.markdown("---")

    # ========================================================================
    # SIDEBAR - Exam settings
    # ========================================================================
    st.sidebar.markdown("### ⚙️ Configurações")
    
    # Anos disponíveis (dinâmico baseado no ano atual)
    current_year = date.today().year
    available_years = list(range(current_year, 2013, -1))
    
    selected_year = st.sidebar.selectbox(
        "Selecione o ano da prova:",
        available_years,
        key="selected_year"
    )
    
    # ========================================================================
    # LOAD EXAM DATA
    # ========================================================================
    try:
        df_exam = load_exam(selected_year)
    except FileNotFoundError:
        st.error(f"❌ Prova do ano {selected_year} não encontrada.")
        st.info("💡 Verifique se o arquivo CSV existe no diretório `data/`.")
        return
    except Exception as e:
        st.error(f"❌ Erro ao carregar a prova: {str(e)}")
        return
    
    if df_exam is None or df_exam.empty:
        st.error("❌ Não foi possível carregar a prova selecionada.")
        return
    
    # ========================================================================
    # PAGINATION SETUP
    # ========================================================================
    total_questions = len(df_exam)
    questions_per_page = 10
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Estatísticas")
    st.sidebar.markdown(f"**Total de questões:** {total_questions}")
    st.sidebar.markdown(f"**Página atual:** {st.session_state.current_page + 1} de {total_pages}")
    st.sidebar.markdown(f"**Questões respondidas:** {len(st.session_state.answers)}")
    
    # Progresso
    progress = len(st.session_state.answers) / total_questions if total_questions > 0 else 0
    st.sidebar.progress(progress)
    st.sidebar.markdown(f"**Progresso:** {progress * 100:.1f}%")
    
    # ========================================================================
    # DISPLAY QUESTIONS
    # ========================================================================
    start = st.session_state.current_page * questions_per_page
    end = min(start + questions_per_page, total_questions)
    
    st.markdown(f"## 📝 Questões {start + 1} a {end}")
    st.markdown(f"**Ano da prova:** {selected_year}")
    st.markdown("---")
    
    for idx in range(start, end):
        question = df_exam.iloc[idx]
        display_question(question, idx)
    
    # ========================================================================
    # NAVIGATION
    # ========================================================================
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Anterior", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
    
    with col2:
        st.markdown(
            f"<p style='text-align: center;'>Página {st.session_state.current_page + 1} de {total_pages}</p>",
            unsafe_allow_html=True
        )
    
    with col3:
        if st.session_state.current_page < total_pages - 1:
            if st.button("Próxima ➡️", use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
    
    # ========================================================================
    # SIDEBAR - Reset answers
    # ========================================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Ações")
    
    if st.sidebar.button("🗑️ Limpar todas as respostas", use_container_width=True):
        st.session_state.answers = {}
        st.session_state.verified = {}
        st.session_state.current_page = 0
        st.success("✅ Todas as respostas foram limpas!")
        st.rerun()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Função principal que controla o fluxo da aplicação.
    - Se não estiver logado, mostra página de login.
    - Se estiver logado, mostra menu topo + página selecionada (Início ou Provas Anteriores).
    """
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Primeiro mostra o menu superior
        show_top_menu()

        # Depois, decide qual "view" mostrar
        view = st.session_state.get("current_view", "inicio")

        if view == "inicio":
            show_home_page()
        elif view == "provas_anteriores":
            show_old_exams_page()
        else:
            # fallback de segurança
            show_home_page()


if __name__ == "__main__":
    main()