"""
Global Job Market Intelligence Platform — Configuration
=========================================================
Environment-aware, validated configuration with sensible defaults.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# ── Environment ──────────────────────────────────────────────────────
ENV = os.getenv("APP_ENV", "production").lower()
DEBUG = ENV == "development"

# ── Paths ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"

for d in [RAW_DIR, PROCESSED_DIR, MODEL_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API Configuration ────────────────────────────────────────────────
ADZUNA_APP_ID: str | None = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY: str | None = os.getenv("ADZUNA_APP_KEY")

COUNTRIES: list[str] = os.getenv("COUNTRIES", "us,gb,in,ca,au,de,sg,fr").split(",")
QUERY: str = os.getenv("QUERY", "data analyst")

# ── UI Theme ─────────────────────────────────────────────────────────
COLORS: list[str] = [
    "#667EEA",
    "#764BA2",
    "#48BB78",
    "#ED8936",
    "#E53E3E",
    "#38B2AC",
    "#D69E2E",
    "#9F7AEA",
    "#FC8181",
    "#4FD1C5",
    "#F6AD55",
    "#68D391",
    "#63B3ED",
    "#B794F4",
    "#FBD38D",
]

GRADIENT_START = "#667EEA"
GRADIENT_END = "#764BA2"

CATEGORY_COLORS: dict[str, str] = {
    "Programming": "#667EEA",
    "Data & Databases": "#764BA2",
    "Big Data": "#48BB78",
    "Cloud & Infrastructure": "#ED8936",
    "ML & AI": "#E53E3E",
    "BI & Visualization": "#38B2AC",
    "Analytics & Statistics": "#D69E2E",
    "DevOps & Tools": "#9F7AEA",
    "Soft Skills": "#FC8181",
}

JOB_TYPE_COLORS: dict[str, str] = {
    "Full-time": "#48BB78",
    "Remote": "#667EEA",
    "Contract": "#ED8936",
    "Hybrid": "#9F7AEA",
    "Part-time": "#D69E2E",
}

SENIORITY_COLORS: dict[str, str] = {
    "Junior": "#4FD1C5",
    "Mid": "#48BB78",
    "Senior": "#667EEA",
    "Lead": "#764BA2",
    "Principal": "#ED8936",
}

SENIORITY_ORDER: list[str] = ["Junior", "Mid", "Senior", "Lead", "Principal"]

# ── App Constants ────────────────────────────────────────────────────
APP_TITLE = "Global Job Market Intelligence Platform"
APP_ICON = "🌍"
APP_VERSION = "2.0.0"
PROCESSED_DATA_PATH = PROCESSED_DIR / "jobs_processed.csv"
RAW_DATA_PATH = RAW_DIR / "jobs_raw.csv"
MODEL_PATH = MODEL_DIR / "salary_model.pkl"
MODEL_META_PATH = MODEL_DIR / "model_metadata.json"

# ── Limits ───────────────────────────────────────────────────────────
MAX_UPLOAD_SIZE_MB = 50
JOB_EXPLORER_PAGE_SIZE = 50
TOP_SKILLS_COUNT = 25
TOP_CITIES_COUNT = 20
HEATMAP_SKILL_COUNT = 15
COOCCURRENCE_PAIR_COUNT = 15
SYNTHETIC_JOB_COUNT = 5000

# ── Model Hyperparameters ────────────────────────────────────────────
MODEL_N_ESTIMATORS = 200
MODEL_MAX_DEPTH = 5
MODEL_LEARNING_RATE = 0.1
MODEL_TEST_SIZE = 0.2
MODEL_RANDOM_STATE = 42
MODEL_CV_FOLDS = 5

# ── Logging ──────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# ── Country ISO Mapping ──────────────────────────────────────────────
COUNTRY_ISO: dict[str, str] = {
    "United States": "USA",
    "United Kingdom": "GBR",
    "India": "IND",
    "Canada": "CAN",
    "Australia": "AUS",
    "Germany": "DEU",
    "Singapore": "SGP",
    "France": "FRA",
}
