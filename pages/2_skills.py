
import streamlit as st
import pandas as pd

df = pd.read_csv("data/jobs_processed.csv")

skills = df["skills"].str.split(",", expand=True).stack()

st.title("🧠 Skill Demand Analysis")

st.bar_chart(skills.value_counts().head(10))
