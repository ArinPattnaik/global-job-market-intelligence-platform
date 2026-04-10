"""
Page 4: Geographic Insights
==============================
Country-level analytics, city breakdowns, and regional comparisons.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Geographic Insights | GJMIP", page_icon="🌍", layout="wide")

with st.sidebar:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

COUNTRY_ISO = {
    "United States": "USA", "United Kingdom": "GBR", "India": "IND",
    "Canada": "CAN", "Australia": "AUS", "Germany": "DEU",
    "Singapore": "SGP", "France": "FRA",
}

@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "processed" / "jobs_processed.csv"
    try:
        return pd.read_csv(path, parse_dates=["posted_date"])
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">🌍 Geographic Insights</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        Regional hiring patterns and comparisons
    </span>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4 = st.columns(4)
top_country = df["country_name"].value_counts().index[0]
top_city = df["city"].value_counts().index[0]
with k1:
    st.metric("Countries Tracked", f"{df['country_name'].nunique()}")
with k2:
    st.metric("Cities Covered", f"{df['city'].nunique()}")
with k3:
    st.metric("Highest Demand", top_country)
with k4:
    st.metric("Top City", top_city)

st.markdown("")

# ── World Choropleth ─────────────────────────────────────────────────
st.markdown("#### 🗺️ Global Job Distribution")

geo_df = df.groupby("country_name").agg(
    jobs=("job_id", "count"),
    avg_salary=("salary_avg", "mean"),
).reset_index()
geo_df["iso_alpha"] = geo_df["country_name"].map(COUNTRY_ISO)

fig_map = px.choropleth(
    geo_df,
    locations="iso_alpha",
    color="jobs",
    hover_name="country_name",
    hover_data={"jobs": ":,", "avg_salary": ":$,.0f", "iso_alpha": False},
    color_continuous_scale=["#0E1117", "#667EEA", "#764BA2"],
    template="plotly_dark",
    labels={"jobs": "Job Count", "avg_salary": "Avg Salary"},
)
fig_map.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(102,126,234,0.2)",
        landcolor="#161B22",
        showland=True,
        showocean=True,
        oceancolor="#0E1117",
        projection_type="natural earth",
    ),
    font=dict(family="Inter", color="#E6EDF3"),
    margin=dict(l=0, r=0, t=10, b=0), height=420,
    coloraxis_showscale=True,
)
st.plotly_chart(fig_map, use_container_width=True)

# ── Country Comparison ───────────────────────────────────────────────
st.markdown("#### 📊 Country Comparison")

country_stats = df.groupby("country_name").agg(
    total_jobs=("job_id", "count"),
    avg_salary=("salary_avg", "mean"),
    median_salary=("salary_avg", "median"),
    companies=("company", "nunique"),
    remote_pct=("job_type", lambda x: (x == "Remote").sum() / len(x) * 100),
).reset_index().sort_values("total_jobs", ascending=False)
country_stats["avg_salary"] = country_stats["avg_salary"].apply(lambda x: f"${x:,.0f}")
country_stats["median_salary"] = country_stats["median_salary"].apply(lambda x: f"${x:,.0f}")
country_stats["remote_pct"] = country_stats["remote_pct"].apply(lambda x: f"{x:.1f}%")
country_stats.columns = ["Country", "Total Jobs", "Avg Salary", "Median Salary", "Companies", "Remote %"]

st.dataframe(country_stats, use_container_width=True, hide_index=True)

# ── Top Cities ───────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏙️ Top 20 Cities by Job Count")
    city_df = df.groupby(["city", "country_name"]).size().reset_index(name="Jobs")
    city_df = city_df.sort_values("Jobs", ascending=False).head(20)
    city_df["Label"] = city_df["city"] + " (" + city_df["country_name"].str[:2].str.upper() + ")"

    fig_city = px.bar(
        city_df, x="Jobs", y="Label", orientation="h",
        color="country_name",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
    )
    fig_city.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=20, t=10, b=0), height=500,
        yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, title=""),
    )
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    st.markdown("#### 💰 Avg Salary by City (Top 20)")
    city_sal = df.groupby(["city", "country_name"])["salary_avg"].agg(["mean", "count"]).reset_index()
    city_sal.columns = ["City", "Country", "Avg Salary", "Jobs"]
    city_sal = city_sal[city_sal["Jobs"] >= 10].sort_values("Avg Salary", ascending=False).head(20)
    city_sal["Label"] = city_sal["City"] + " (" + city_sal["Country"].str[:2].str.upper() + ")"

    fig_city_sal = px.bar(
        city_sal, x="Avg Salary", y="Label", orientation="h",
        color="Country",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
        hover_data=["Jobs"],
    )
    fig_city_sal.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=20, t=10, b=0), height=500,
        yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, title=""),
    )
    st.plotly_chart(fig_city_sal, use_container_width=True)

# ── Job Type by Country ──────────────────────────────────────────────
st.markdown("#### 🏷️ Job Type Distribution by Country")
jt_country = df.groupby(["country_name", "job_type"]).size().reset_index(name="Count")
fig_jt = px.bar(
    jt_country, x="country_name", y="Count", color="job_type",
    barmode="stack",
    color_discrete_sequence=COLORS,
    template="plotly_dark",
    labels={"country_name": "Country", "job_type": "Job Type"},
)
fig_jt.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E6EDF3"),
    margin=dict(l=0, r=0, t=10, b=0), height=350,
    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, title=""),
)
st.plotly_chart(fig_jt, use_container_width=True)
