
import requests
import pandas as pd
from config.settings import ADZUNA_APP_ID, ADZUNA_APP_KEY, COUNTRIES, QUERY

def fetch_jobs():
    jobs = []

    for country in COUNTRIES:
        for page in range(1,5):
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": QUERY
            }

            r = requests.get(url, params=params).json()

            for job in r.get("results", []):
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
    df.to_csv("data/jobs_raw.csv", index=False)
    print("Jobs fetched:", len(df))

if __name__ == "__main__":
    fetch_jobs()
