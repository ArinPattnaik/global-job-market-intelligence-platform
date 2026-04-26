"""
Adzuna Job Fetcher
====================
Fetches job postings from the Adzuna API with retry logic and validation.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.logging_config import get_logger
from config.settings import (
    ADZUNA_APP_ID,
    ADZUNA_APP_KEY,
    COUNTRIES,
    QUERY,
    RAW_DATA_PATH,
)

logger = get_logger("fetch_jobs")

_BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
_PAGES_PER_COUNTRY = 4
_REQUEST_TIMEOUT = 30  # seconds


def _build_session() -> requests.Session:
    """Create a requests session with automatic retries."""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _validate_credentials() -> None:
    """Ensure API credentials are configured."""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise OSError("ADZUNA_APP_ID and ADZUNA_APP_KEY must be set in .env")


def _parse_job(job: dict[str, Any], country: str) -> dict[str, Any]:
    """Extract relevant fields from a single API result."""
    return {
        "title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "country": country,
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "description": job.get("description"),
        "posted_date": job.get("created"),
    }


def fetch_jobs() -> pd.DataFrame:
    """
    Fetch jobs from Adzuna API for all configured countries.

    Returns the fetched DataFrame and saves it to the raw data path.
    """
    _validate_credentials()

    session = _build_session()
    jobs: list[dict[str, Any]] = []

    for country in COUNTRIES:
        logger.info("Fetching jobs for country=%s, query=%s", country, QUERY)
        for page in range(1, _PAGES_PER_COUNTRY + 1):
            url = _BASE_URL.format(country=country, page=page)
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": QUERY,
            }
            try:
                resp = session.get(url, params=params, timeout=_REQUEST_TIMEOUT)
                resp.raise_for_status()
                data = resp.json()
                page_jobs = [_parse_job(j, country) for j in data.get("results", [])]
                jobs.extend(page_jobs)
                logger.debug("  page %d: %d results", page, len(page_jobs))
            except requests.RequestException:
                logger.exception("Failed to fetch page %d for %s", page, country)
                continue

    df = pd.DataFrame(jobs)
    if not df.empty:
        RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(RAW_DATA_PATH, index=False)
        logger.info("Saved %d raw jobs → %s", len(df), RAW_DATA_PATH)
    else:
        logger.warning("No jobs fetched from API")

    return df


if __name__ == "__main__":
    fetch_jobs()
