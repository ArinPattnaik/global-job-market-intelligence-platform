
import streamlit as st
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="logs/skills.log", format="%(asctime)s - %(levelname)s - %(message)s")
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

if not df.empty:
    df = df.dropna(subset=["skills"])
    skills = df["skills"].str.split(",", expand=True).stack()
    st.title("🧠 Skill Demand Analysis")
    st.bar_chart(skills.value_counts().head(10))
else:
    st.warning("No data available.")
