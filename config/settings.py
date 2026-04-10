"""
Global Job Market Intelligence Platform — Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for d in [RAW_DIR, PROCESSED_DIR, MODEL_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API Configuration ────────────────────────────────────────────────
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
COUNTRIES = os.getenv("COUNTRIES", "us,gb,in,ca,au,de,sg,fr").split(",")
QUERY = os.getenv("QUERY", "data analyst")

# ── Color Palette ────────────────────────────────────────────────────
COLORS = [
    "#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
    "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5",
    "#F6AD55", "#68D391", "#63B3ED", "#B794F4", "#FBD38D",
]

GRADIENT_START = "#667EEA"
GRADIENT_END = "#764BA2"

# ── App Constants ────────────────────────────────────────────────────
APP_TITLE = "Global Job Market Intelligence Platform"
APP_ICON = "🌍"
PROCESSED_DATA_PATH = PROCESSED_DIR / "jobs_processed.csv"
RAW_DATA_PATH = RAW_DIR / "jobs_raw.csv"
MODEL_PATH = MODEL_DIR / "salary_model.pkl"
