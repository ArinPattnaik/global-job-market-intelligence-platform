
import streamlit as st
import pandas as pd
import plotly.express as px
import logging

logging.basicConfig(level=logging.INFO, filename="logs/dashboard.log", format="%(asctime)s - %(levelname)s - %(message)s")
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
    st.title("📊 Global Hiring Dashboard")
    st.metric("Total Jobs", len(df))
    st.subheader("Jobs by Country")
    fig = px.bar(df["country"].value_counts())
    st.plotly_chart(fig)
    st.subheader("Top Hiring Companies")
    fig2 = px.bar(df["company"].value_counts().head(10))
    st.plotly_chart(fig2)
else:
    st.warning("No data available.")
