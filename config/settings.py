"""
Configuration settings for the CFS Online Exam System
"""
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data directory
DATA_DIR = ROOT_DIR / "data"

# CSV file with all exams and answer keys
EXAMS_FILE = DATA_DIR / "provas_cfs_com_gabarito.csv"  # ou "exams_with_answers.csv" se renomear

# Available exam years
AVAILABLE_YEARS = list(range(2025, 2013, -1))

# Pagination settings
QUESTIONS_PER_PAGE = 10

# Answer options
ANSWER_OPTIONS = ['A', 'B', 'C', 'D']