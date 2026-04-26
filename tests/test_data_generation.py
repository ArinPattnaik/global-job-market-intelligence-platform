"""
Tests for Synthetic Data Generation
======================================
Validates data quality, schema, and distribution properties.
"""

import pandas as pd
import pytest

from data.generate_synthetic_data import (
    COUNTRIES,
    JOB_TYPES,
    ROLES,
    SENIORITY,
    generate_jobs,
)


@pytest.fixture(scope="module")
def generated_df() -> pd.DataFrame:
    """Generate a small dataset for testing (faster than 5000)."""
    return generate_jobs(n=500)


class TestDataSchema:
    """Verify the generated DataFrame has the correct structure."""

    EXPECTED_COLUMNS = {
        "job_id",
        "title",
        "category",
        "seniority",
        "company",
        "city",
        "country",
        "country_name",
        "location",
        "salary_min",
        "salary_max",
        "salary_avg",
        "description",
        "skills",
        "job_type",
        "experience_years",
        "posted_date",
    }

    def test_has_all_columns(self, generated_df: pd.DataFrame):
        assert self.EXPECTED_COLUMNS.issubset(set(generated_df.columns))

    def test_correct_row_count(self, generated_df: pd.DataFrame):
        assert len(generated_df) == 500

    def test_no_null_job_ids(self, generated_df: pd.DataFrame):
        assert generated_df["job_id"].notna().all()

    def test_unique_job_ids(self, generated_df: pd.DataFrame):
        assert generated_df["job_id"].is_unique


class TestDataQuality:
    """Verify data quality constraints."""

    def test_salary_min_less_than_max(self, generated_df: pd.DataFrame):
        assert (generated_df["salary_min"] <= generated_df["salary_max"]).all()

    def test_salary_avg_between_min_max(self, generated_df: pd.DataFrame):
        df = generated_df
        assert (df["salary_avg"] >= df["salary_min"]).all()
        assert (df["salary_avg"] <= df["salary_max"]).all()

    def test_positive_salaries(self, generated_df: pd.DataFrame):
        assert (generated_df["salary_min"] > 0).all()

    def test_experience_non_negative(self, generated_df: pd.DataFrame):
        assert (generated_df["experience_years"] >= 0).all()

    def test_skills_not_empty(self, generated_df: pd.DataFrame):
        # Every job should have at least some skills
        assert generated_df["skills"].notna().all()
        assert (generated_df["skills"].str.len() > 0).all()

    def test_valid_countries(self, generated_df: pd.DataFrame):
        valid_codes = set(COUNTRIES.keys())
        assert set(generated_df["country"].unique()).issubset(valid_codes)

    def test_valid_seniority_levels(self, generated_df: pd.DataFrame):
        valid = set(SENIORITY.keys())
        assert set(generated_df["seniority"].unique()).issubset(valid)

    def test_valid_job_types(self, generated_df: pd.DataFrame):
        valid = set(JOB_TYPES.keys())
        assert set(generated_df["job_type"].unique()).issubset(valid)

    def test_valid_categories(self, generated_df: pd.DataFrame):
        valid = set(ROLES.keys())
        assert set(generated_df["category"].unique()).issubset(valid)

    def test_descriptions_not_empty(self, generated_df: pd.DataFrame):
        assert generated_df["description"].notna().all()
        assert (generated_df["description"].str.len() > 50).all()

    def test_posted_dates_valid(self, generated_df: pd.DataFrame):
        dates = pd.to_datetime(generated_df["posted_date"])
        assert dates.notna().all()
