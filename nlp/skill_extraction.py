"""
Enhanced NLP Skill Extraction
================================
80+ skill taxonomy with categorization for job description analysis.
"""

import pandas as pd
import re
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Skill Taxonomy (80+ skills organized by category) ────────────────

SKILL_TAXONOMY = {
    "Programming": [
        "python", "r", "java", "scala", "go", "rust", "julia", "c++",
        "javascript", "typescript", "bash", "shell", "matlab",
    ],
    "Data & Databases": [
        "sql", "nosql", "mongodb", "postgresql", "mysql", "redis",
        "elasticsearch", "cassandra", "dynamodb", "neo4j",
    ],
    "Big Data": [
        "spark", "hadoop", "kafka", "flink", "hive", "airflow", "dbt",
        "nifi", "presto", "trino",
    ],
    "Cloud & Infrastructure": [
        "aws", "azure", "gcp", "snowflake", "databricks", "bigquery",
        "redshift", "docker", "kubernetes", "terraform",
    ],
    "ML & AI": [
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "keras", "xgboost", "lightgbm", "mlflow",
        "huggingface", "nlp", "computer vision", "reinforcement learning",
        "llm", "transformers",
    ],
    "BI & Visualization": [
        "tableau", "power bi", "looker", "metabase", "superset", "qlik",
        "data visualization", "d3.js",
    ],
    "Analytics & Statistics": [
        "statistics", "a/b testing", "data modeling", "etl",
        "data visualization", "excel", "google analytics",
        "requirements gathering", "stakeholder management",
    ],
    "DevOps & Tools": [
        "ci/cd", "git", "jenkins", "ansible", "linux", "jira",
        "confluence", "fastapi", "flask",
    ],
    "Soft Skills": [
        "leadership", "agile", "strategy", "research",
    ],
}

# Flatten for fast lookup
ALL_SKILLS = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        ALL_SKILLS[skill] = category


def extract_skills(text: str) -> str:
    """Extract skills from a job description text."""
    if not text or pd.isna(text):
        return ""
    text_lower = str(text).lower()
    found = []
    for skill in ALL_SKILLS:
        if skill in found:
            continue
        # Use word-boundary regex for short skills to avoid false positives
        if len(skill) <= 3:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        else:
            if skill in text_lower:
                found.append(skill)
    return ",".join(found)


def get_skill_category(skill: str) -> str:
    """Get the category for a given skill."""
    return ALL_SKILLS.get(skill.lower().strip(), "Other")


def get_all_categories() -> list:
    """Return all skill categories."""
    return list(SKILL_TAXONOMY.keys())


def process() -> None:
    """Process raw jobs data to extract skills."""
    try:
        base_dir = Path(__file__).resolve().parent.parent
        raw_path = base_dir / "data" / "raw" / "jobs_raw.csv"
        processed_path = base_dir / "data" / "processed" / "jobs_processed.csv"

        df = pd.read_csv(raw_path)
        df["skills"] = df["description"].apply(extract_skills)
        df.to_csv(processed_path, index=False)
        logger.info(f"Skills extracted for {len(df)} jobs → {processed_path}")
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        raise


if __name__ == "__main__":
    process()
