
import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
COUNTRIES = os.getenv("COUNTRIES", "us,gb,in,ca,au").split(",")
QUERY = os.getenv("QUERY", "data analyst")
