"""
CFS Online Exam System - Main Application
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(page_title="CFS Online Exam", layout="wide")

# File paths - using relative paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
EXAMS_FILE = DATA_DIR / "exams_with_answers.csv"

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'verified' not in st.session_state:
    st.session_state.verified = {}


def load_exam(year):
    """Load CSV file and filter by year"""
    try:
        df = pd.read_csv(EXAMS_FILE, encoding='utf-8')
    except:
        df = pd.read_csv(EXAMS_FILE, encoding='latin-1')
    
    df.columns = df.columns.str.lower().str.strip()
    return df[df['ano'] == year]


def display_question(question, idx):
    """Display a question with its alternatives and verification button"""
    st.markdown(f"### Question {question['numero']} - {question.get('disciplina', 'N/A')}")
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
    
    current_answer = st.session_state.answers.get(key, None)
    answer = st.radio(
        "Select your answer:",
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


def main():
    st.title("🎓 CFS Online Exam")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Settings")
    available_years = list(range(2025, 2013, -1))
    selected_year = st.sidebar.selectbox("Select exam year:", available_years)
    
    df_exam = load_exam(selected_year)
    
    if df_exam is None or df_exam.empty:
        st.error("Could not load the selected exam.")
        return
    
    total_questions = len(df_exam)
    questions_per_page = 10
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    
    # Sidebar info
    st.sidebar.markdown(f"**Total questions:** {total_questions}")
    st.sidebar.markdown(f"**Current page:** {st.session_state.current_page + 1} of {total_pages}")
    st.sidebar.markdown(f"**Answered questions:** {len(st.session_state.answers)}")
    
    start = st.session_state.current_page * questions_per_page
    end = min(start + questions_per_page, total_questions)
    
    st.markdown(f"## Questions {start + 1} to {end}")
    for idx in range(start, end):
        question = df_exam.iloc[idx]
        display_question(question, idx)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_page -= 1
                st.rerun()
    with col3:
        if st.session_state.current_page < total_pages - 1:
            if st.button("Next ➡️"):
                st.session_state.current_page += 1
                st.rerun()
    
    # Reset answers
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Clear all answers"):
        st.session_state.answers = {}
        st.session_state.verified = {}
        st.session_state.current_page = 0
        st.rerun()


if __name__ == "__main__":
    main()