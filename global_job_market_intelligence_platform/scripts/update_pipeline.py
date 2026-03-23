
# Example cron usage:
# 0 0 * * * python scripts/update_pipeline.py

import os

os.system("python etl/fetch_jobs.py")
os.system("python nlp/skill_extraction.py")
