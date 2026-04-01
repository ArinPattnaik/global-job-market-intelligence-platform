
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="logs/skill_extraction.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

skills_list = [
    "python", "sql", "power bi", "tableau", "excel", "machine learning",
    "statistics", "pandas", "numpy", "spark", "aws", "data visualization"
]

def extract_skills(text: str) -> str:
    """Extract skills from job description text."""
    text = str(text).lower()
    found = []
    for s in skills_list:
        if s in text:
            found.append(s)
    return ",".join(found)

def process() -> None:
    """Process jobs data to extract skills."""
    try:
        df = pd.read_csv("data/raw/jobs_raw.csv")
        df["skills"] = df["description"].apply(extract_skills)
        df.to_csv("data/processed/jobs_processed.csv", index=False)
        logger.info("Skills extracted")
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        raise

if __name__ == "__main__":
    process()
