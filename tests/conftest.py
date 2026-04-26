"""
Shared test fixtures for the GJMIP test suite.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_jobs_df() -> pd.DataFrame:
    """A small DataFrame mimicking the processed jobs CSV."""
    return pd.DataFrame(
        {
            "job_id": ["JOB-00001", "JOB-00002", "JOB-00003"],
            "title": ["Senior Data Scientist", "Data Analyst", "ML Engineer"],
            "category": ["Data Scientist", "Data Analyst", "ML Engineer"],
            "seniority": ["Senior", "Mid", "Senior"],
            "company": ["Google", "Meta", "OpenAI"],
            "city": ["San Francisco", "New York", "San Francisco"],
            "country": ["us", "us", "us"],
            "country_name": ["United States", "United States", "United States"],
            "location": [
                "San Francisco, United States",
                "New York, United States",
                "San Francisco, United States",
            ],
            "salary_min": [140000, 80000, 160000],
            "salary_max": [180000, 110000, 200000],
            "salary_avg": [160000, 95000, 180000],
            "description": [
                "We need python and machine learning skills",
                "SQL and excel required for data analysis",
                "Deep learning with pytorch and docker",
            ],
            "skills": [
                "python,machine learning,statistics",
                "sql,excel,data visualization",
                "python,deep learning,pytorch,docker",
            ],
            "job_type": ["Full-time", "Remote", "Full-time"],
            "experience_years": [7, 3, 8],
            "posted_date": pd.to_datetime(
                ["2025-01-15", "2025-02-01", "2025-01-20"]
            ),
        }
    )
