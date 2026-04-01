
import streamlit as st
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="logs/job_search.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/processed/jobs_processed.csv")
    except FileNotFoundError:
        st.error("Data not found. Please run the ETL pipeline first.")
        logger.error("Data file not found")
        return pd.DataFrame()

df = load_data()

st.title("🔎 Job Search")

title = st.text_input("Search Job Title")

if not df.empty:
    if title:
        results = df[df["title"].str.contains(title, case=False, na=False)]
    else:
        results = df
    st.dataframe(results.head(50))
else:
    st.warning("No data available.")
