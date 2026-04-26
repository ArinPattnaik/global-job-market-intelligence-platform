"""
Centralized Data Loading
==========================
Single source of truth for loading and validating the processed dataset.
Eliminates duplicated load_data() across every page.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from config.logging_config import get_logger
from config.settings import PROCESSED_DATA_PATH

logger = get_logger("data_loader")

_REQUIRED_COLUMNS = {
    "job_id", "title", "category", "seniority", "company",
    "city", "country", "country_name", "location",
    "salary_min", "salary_max", "salary_avg",
    "skills", "job_type", "experience_years", "posted_date",
}


@st.cache_data(ttl=3600, show_spinner="Loading data…")
def load_processed_data(
    path: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load the processed jobs CSV with validation.

    Returns an empty DataFrame on failure rather than crashing.
    """
    data_path = Path(path) if path else PROCESSED_DATA_PATH

    try:
        if not data_path.exists():
            logger.warning("Data file not found: %s", data_path)
            return pd.DataFrame()

        df = pd.read_csv(data_path, parse_dates=["posted_date"])

        # Validate required columns
        missing = _REQUIRED_COLUMNS - set(df.columns)
        if missing:
            logger.error("Missing required columns: %s", missing)
            return pd.DataFrame()

        # Basic data quality checks
        initial_len = len(df)
        df = df.dropna(subset=["job_id", "title", "salary_avg"])
        dropped = initial_len - len(df)
        if dropped > 0:
            logger.info(
                "Dropped %d rows with missing critical fields", dropped
            )

        # Ensure numeric types
        for col in ("salary_min", "salary_max", "salary_avg", "experience_years"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

        logger.info(
            "Loaded %d jobs from %s (%d countries, %d companies)",
            len(df),
            data_path.name,
            df["country_name"].nunique(),
            df["company"].nunique(),
        )
        return df

    except Exception:
        logger.exception("Failed to load data from %s", data_path)
        return pd.DataFrame()


def require_data(df: pd.DataFrame) -> None:
    """Show a warning and stop the page if the DataFrame is empty."""
    if df.empty:
        st.warning(
            "⚠️ No data available. Run "
            "`python data/generate_synthetic_data.py` to generate sample data."
        )
        st.stop()
