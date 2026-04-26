"""
Pipeline Orchestrator
=======================
Runs the full ETL → NLP → Model Training pipeline.

Usage:
    python scripts/update_pipeline.py
    # Or via cron: 0 0 * * * python scripts/update_pipeline.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.logging_config import get_logger

logger = get_logger("pipeline")


def run_pipeline(skip_fetch: bool = False) -> None:
    """
    Execute the data pipeline end-to-end.

    Parameters
    ----------
    skip_fetch : bool
        If True, skip the API fetch step (useful when using synthetic data).
    """
    start = time.perf_counter()
    logger.info("=" * 60)
    logger.info("Pipeline started")

    # Step 1: Fetch (optional)
    if not skip_fetch:
        try:
            from etl.fetch_jobs import fetch_jobs
            logger.info("[1/3] Fetching jobs from API…")
            fetch_jobs()
        except Exception:
            logger.exception("ETL fetch failed — continuing with existing data")
    else:
        logger.info("[1/3] Skipping API fetch (skip_fetch=True)")

    # Step 2: NLP skill extraction
    try:
        from nlp.skill_extraction import process as extract_skills
        logger.info("[2/3] Extracting skills…")
        extract_skills()
    except Exception:
        logger.exception("Skill extraction failed")
        raise

    # Step 3: Model training
    try:
        from models.train_model import train_model
        logger.info("[3/3] Training salary model…")
        train_model()
    except Exception:
        logger.exception("Model training failed")
        raise

    elapsed = time.perf_counter() - start
    logger.info("Pipeline completed in %.1fs", elapsed)
    logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline(skip_fetch="--skip-fetch" in sys.argv)
