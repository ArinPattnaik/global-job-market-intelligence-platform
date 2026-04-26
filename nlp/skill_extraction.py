"""
Enhanced NLP Skill Extraction
================================
80+ skill taxonomy with categorization for job description analysis.
Uses compiled regex patterns for performance.
"""

from __future__ import annotations

import re

import pandas as pd

from config.logging_config import get_logger

logger = get_logger("skill_extraction")

# ── Skill Taxonomy (80+ skills organized by category) ────────────────

SKILL_TAXONOMY: dict[str, list[str]] = {
    "Programming": [
        "python",
        "r",
        "java",
        "scala",
        "go",
        "rust",
        "julia",
        "c++",
        "javascript",
        "typescript",
        "bash",
        "shell",
        "matlab",
    ],
    "Data & Databases": [
        "sql",
        "nosql",
        "mongodb",
        "postgresql",
        "mysql",
        "redis",
        "elasticsearch",
        "cassandra",
        "dynamodb",
        "neo4j",
    ],
    "Big Data": [
        "spark",
        "hadoop",
        "kafka",
        "flink",
        "hive",
        "airflow",
        "dbt",
        "nifi",
        "presto",
        "trino",
    ],
    "Cloud & Infrastructure": [
        "aws",
        "azure",
        "gcp",
        "snowflake",
        "databricks",
        "bigquery",
        "redshift",
        "docker",
        "kubernetes",
        "terraform",
    ],
    "ML & AI": [
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "keras",
        "xgboost",
        "lightgbm",
        "mlflow",
        "huggingface",
        "nlp",
        "computer vision",
        "reinforcement learning",
        "llm",
        "transformers",
    ],
    "BI & Visualization": [
        "tableau",
        "power bi",
        "looker",
        "metabase",
        "superset",
        "qlik",
        "data visualization",
        "d3.js",
    ],
    "Analytics & Statistics": [
        "statistics",
        "a/b testing",
        "data modeling",
        "etl",
        "excel",
        "google analytics",
        "requirements gathering",
        "stakeholder management",
    ],
    "DevOps & Tools": [
        "ci/cd",
        "git",
        "jenkins",
        "ansible",
        "linux",
        "jira",
        "confluence",
        "fastapi",
        "flask",
    ],
    "Soft Skills": [
        "leadership",
        "agile",
        "strategy",
        "research",
    ],
}

# ── Derived lookups (built once at import time) ──────────────────────

ALL_SKILLS: dict[str, str] = {}
for _category, _skills in SKILL_TAXONOMY.items():
    for _skill in _skills:
        ALL_SKILLS[_skill] = _category

# Pre-compile regex patterns for each skill (significant perf gain)
_SKILL_PATTERNS: dict[str, re.Pattern[str]] = {}
for _skill in ALL_SKILLS:
    if len(_skill) <= 3:
        _SKILL_PATTERNS[_skill] = re.compile(r"\b" + re.escape(_skill) + r"\b", re.IGNORECASE)
    else:
        # For longer skills a simple substring check is fine and faster
        _SKILL_PATTERNS[_skill] = re.compile(re.escape(_skill), re.IGNORECASE)


def extract_skills(text: str | None) -> str:
    """
    Extract skills from a job description text.

    Returns a comma-separated string of matched skill names (lowercase).
    Returns an empty string when no skills are found or input is invalid.
    """
    if not text or (isinstance(text, float) and pd.isna(text)):
        return ""

    text_str = str(text)
    found: list[str] = []

    for skill, pattern in _SKILL_PATTERNS.items():
        if pattern.search(text_str):
            found.append(skill)

    return ",".join(found)


def get_skill_category(skill: str) -> str:
    """Get the category for a given skill."""
    return ALL_SKILLS.get(skill.lower().strip(), "Other")


def get_all_categories() -> list[str]:
    """Return all skill categories."""
    return list(SKILL_TAXONOMY.keys())


def process() -> None:
    """Process raw jobs data to extract skills."""
    from pathlib import Path

    base_dir = Path(__file__).resolve().parent.parent
    raw_path = base_dir / "data" / "raw" / "jobs_raw.csv"
    processed_path = base_dir / "data" / "processed" / "jobs_processed.csv"

    try:
        df = pd.read_csv(raw_path)
        df["skills"] = df["description"].apply(extract_skills)
        df.to_csv(processed_path, index=False)
        logger.info("Skills extracted for %d jobs → %s", len(df), processed_path)
    except FileNotFoundError:
        logger.error("Raw data file not found: %s", raw_path)
        raise
    except Exception:
        logger.exception("Error during skill extraction pipeline")
        raise


if __name__ == "__main__":
    process()
