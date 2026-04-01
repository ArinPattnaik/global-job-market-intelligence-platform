
import requests
import pandas as pd
import logging
from config.settings import ADZUNA_APP_ID, ADZUNA_APP_KEY, COUNTRIES, QUERY

logging.basicConfig(level=logging.INFO, filename="logs/fetch_jobs.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_jobs() -> None:
    """Fetch jobs from Adzuna API and save to CSV."""
    jobs = []
    try:
        for country in COUNTRIES:
            for page in range(1, 5):
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
                params = {
                    "app_id": ADZUNA_APP_ID,
                    "app_key": ADZUNA_APP_KEY,
                    "what": QUERY
                }
                r = requests.get(url, params=params)
                r.raise_for_status()
                data = r.json()
                for job in data.get("results", []):
                    jobs.append({
                        "title": job.get("title"),
                        "company": job.get("company", {}).get("display_name"),
                        "location": job.get("location", {}).get("display_name"),
                        "country": country,
                        "salary_min": job.get("salary_min"),
                        "salary_max": job.get("salary_max"),
                        "description": job.get("description"),
                        "posted_date": job.get("created")
                    })
        df = pd.DataFrame(jobs)
        df.to_csv("data/raw/jobs_raw.csv", index=False)
        logger.info(f"Jobs fetched: {len(df)}")
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise

if __name__ == "__main__":
    fetch_jobs()
