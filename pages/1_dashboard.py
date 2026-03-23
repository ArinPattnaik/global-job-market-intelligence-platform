
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/jobs_processed.csv")

st.title("📊 Global Hiring Dashboard")

st.metric("Total Jobs", len(df))

st.subheader("Jobs by Country")
fig = px.bar(df["country"].value_counts())
st.plotly_chart(fig)

st.subheader("Top Hiring Companies")
fig2 = px.bar(df["company"].value_counts().head(10))
st.plotly_chart(fig2)
