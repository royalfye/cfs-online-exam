from pathlib import Path

import pandas as pd


# Definição de caminhos
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
EXAMS_FILE = DATA_DIR / "exams_with_answers.csv"


def load_exam(year: int) -> pd.DataFrame:
    """
    Carrega o CSV de provas e filtra pelo ano informado.
    Retorna um DataFrame apenas com as questões daquele ano.
    """
    try:
        df = pd.read_csv(EXAMS_FILE, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(EXAMS_FILE, encoding="latin-1")

    df.columns = df.columns.str.lower().str.strip()
    return df[df["ano"] == year]