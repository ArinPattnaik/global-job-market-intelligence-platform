
import streamlit as st
import pandas as pd

df = pd.read_csv("data/jobs_processed.csv")

st.title("🔎 Job Search")

title = st.text_input("Search Job Title")

if title:
    results = df[df["title"].str.contains(title, case=False)]
else:
    results = df

st.dataframe(results.head(50))
