"""
Page 4: Geographic Insights
==============================
Country-level analytics, city breakdowns, and regional comparisons.
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from config.settings import COLORS, COUNTRY_ISO, TOP_CITIES_COUNT
from utils.chart_helpers import HEATMAP_SCALE, apply_default_layout, format_currency
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Geographic Insights", "🌍")

df = load_processed_data()
require_data(df)

page_header("🌍", "Geographic Insights", "Regional hiring patterns and comparisons")

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

geo_df = (
    df.groupby("country_name")
    .agg(
        jobs=("job_id", "count"),
        avg_salary=("salary_avg", "mean"),
    )
    .reset_index()
)
geo_df["iso_alpha"] = geo_df["country_name"].map(COUNTRY_ISO)

fig_map = px.choropleth(
    geo_df,
    locations="iso_alpha",
    color="jobs",
    hover_name="country_name",
    hover_data={"jobs": ":,", "avg_salary": ":$,.0f", "iso_alpha": False},
    color_continuous_scale=HEATMAP_SCALE,
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
    margin=dict(l=0, r=0, t=10, b=0),
    height=420,
)
st.plotly_chart(fig_map, use_container_width=True)

# ── Country Comparison Table ─────────────────────────────────────────
st.markdown("#### 📊 Country Comparison")

country_stats = (
    df.groupby("country_name")
    .agg(
        total_jobs=("job_id", "count"),
        avg_salary=("salary_avg", "mean"),
        median_salary=("salary_avg", "median"),
        companies=("company", "nunique"),
        remote_pct=("job_type", lambda x: (x == "Remote").sum() / len(x) * 100),
    )
    .reset_index()
    .sort_values("total_jobs", ascending=False)
)

country_stats["avg_salary"] = country_stats["avg_salary"].apply(format_currency)
country_stats["median_salary"] = country_stats["median_salary"].apply(format_currency)
country_stats["remote_pct"] = country_stats["remote_pct"].apply(lambda x: f"{x:.1f}%")
country_stats.columns = [
    "Country",
    "Total Jobs",
    "Avg Salary",
    "Median Salary",
    "Companies",
    "Remote %",
]
st.dataframe(country_stats, use_container_width=True, hide_index=True)

# ── Top Cities ───────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### 🏙️ Top {TOP_CITIES_COUNT} Cities by Job Count")
    city_df = df.groupby(["city", "country_name"]).size().reset_index(name="Jobs")
    city_df = city_df.sort_values("Jobs", ascending=False).head(TOP_CITIES_COUNT)
    city_df["Label"] = city_df["city"] + " (" + city_df["country_name"].str[:2].str.upper() + ")"

    fig_city = px.bar(
        city_df,
        x="Jobs",
        y="Label",
        orientation="h",
        color="country_name",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
    )
    apply_default_layout(fig_city, height=500, legend_horizontal=True)
    fig_city.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    st.markdown(f"#### 💰 Avg Salary by City (Top {TOP_CITIES_COUNT})")
    city_sal = (
        df.groupby(["city", "country_name"])["salary_avg"].agg(["mean", "count"]).reset_index()
    )
    city_sal.columns = ["City", "Country", "Avg Salary", "Jobs"]
    city_sal = (
        city_sal[city_sal["Jobs"] >= 10]
        .sort_values("Avg Salary", ascending=False)
        .head(TOP_CITIES_COUNT)
    )
    city_sal["Label"] = city_sal["City"] + " (" + city_sal["Country"].str[:2].str.upper() + ")"

    fig_city_sal = px.bar(
        city_sal,
        x="Avg Salary",
        y="Label",
        orientation="h",
        color="Country",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
        hover_data=["Jobs"],
    )
    apply_default_layout(fig_city_sal, height=500, legend_horizontal=True)
    fig_city_sal.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_city_sal, use_container_width=True)

# ── Job Type by Country ──────────────────────────────────────────────
st.markdown("#### 🏷️ Job Type Distribution by Country")
jt_country = df.groupby(["country_name", "job_type"]).size().reset_index(name="Count")
fig_jt = px.bar(
    jt_country,
    x="country_name",
    y="Count",
    color="job_type",
    barmode="stack",
    color_discrete_sequence=COLORS,
    template="plotly_dark",
    labels={"country_name": "Country", "job_type": "Job Type"},
)
apply_default_layout(fig_jt, height=350, legend_horizontal=True)
st.plotly_chart(fig_jt, use_container_width=True)
