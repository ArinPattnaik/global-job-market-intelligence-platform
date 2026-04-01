
# Example cron usage:
# 0 0 * * * python scripts/update_pipeline.py

import subprocess
import logging

logging.basicConfig(level=logging.INFO, filename="logs/update_pipeline.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def update_pipeline() -> None:
    """Update the data pipeline by running ETL and NLP steps."""
    try:
        logger.info("Starting ETL fetch jobs")
        subprocess.run(["python", "etl/fetch_jobs.py"], check=True)
        logger.info("Starting skill extraction")
        subprocess.run(["python", "nlp/skill_extraction.py"], check=True)
        logger.info("Pipeline updated successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    update_pipeline()
