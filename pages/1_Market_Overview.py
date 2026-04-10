"""
Page 1: Market Overview Dashboard
===================================
Interactive dashboard with KPIs, trends, and hiring analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Market Overview | GJMIP", page_icon="📊", layout="wide")

# ── Data Loading ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "processed" / "jobs_processed.csv"
    try:
        df = pd.read_csv(path, parse_dates=["posted_date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

if df.empty:
    st.warning("No data available. Please generate data first.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">📊 Market Overview</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        Global hiring trends and market analytics
    </span>
</div>
""", unsafe_allow_html=True)

# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        countries = st.multiselect(
            "Country", options=sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
        )
    with fc2:
        categories = st.multiselect(
            "Role Category", options=sorted(df["category"].unique()),
            default=sorted(df["category"].unique()),
        )
    with fc3:
        seniorities = st.multiselect(
            "Seniority", options=sorted(df["seniority"].unique()),
            default=sorted(df["seniority"].unique()),
        )

# Apply filters
mask = (
    df["country_name"].isin(countries) &
    df["category"].isin(categories) &
    df["seniority"].isin(seniorities)
)
filtered = df[mask]

if filtered.empty:
    st.info("No data matches the selected filters. Adjust your filters above.")
    st.stop()

# ── KPI Row ──────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Total Jobs", f"{len(filtered):,}")
with k2:
    st.metric("Avg Salary", f"${filtered['salary_avg'].mean():,.0f}")
with k3:
    st.metric("Companies", f"{filtered['company'].nunique():,}")
with k4:
    st.metric("Countries", f"{filtered['country_name'].nunique()}")
with k5:
    remote_pct = (filtered["job_type"] == "Remote").sum() / len(filtered) * 100
    st.metric("Remote %", f"{remote_pct:.1f}%")

st.markdown("")

# ── Trend Chart ──────────────────────────────────────────────────────
st.markdown("#### 📈 Job Postings Over Time")

trend = filtered.groupby(filtered["posted_date"].dt.to_period("W")).size().reset_index()
trend.columns = ["Week", "Jobs"]
trend["Week"] = trend["Week"].dt.to_timestamp()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=trend["Week"], y=trend["Jobs"],
    mode="lines",
    fill="tonexty",
    line=dict(color="#667EEA", width=2.5),
    fillcolor="rgba(102,126,234,0.12)",
    hovertemplate="<b>%{x|%b %d, %Y}</b><br>Jobs: %{y:,}<extra></extra>",
))
fig_trend.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E6EDF3"),
    margin=dict(l=0, r=0, t=10, b=0),
    height=300,
    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    hovermode="x unified",
)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Country & Company ────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 Jobs by Country")
    country_df = filtered["country_name"].value_counts().reset_index()
    country_df.columns = ["Country", "Jobs"]
    fig_country = px.bar(
        country_df, x="Jobs", y="Country", orientation="h",
        color="Jobs", color_continuous_scale=["#1a1f2e", "#667EEA", "#764BA2"],
        template="plotly_dark",
    )
    fig_country.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=0), height=350,
    )
    fig_country.update_yaxes(gridcolor="rgba(102,126,234,0.06)")
    fig_country.update_xaxes(gridcolor="rgba(102,126,234,0.06)")
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    st.markdown("#### 🏢 Top 15 Hiring Companies")
    company_df = filtered["company"].value_counts().head(15).reset_index()
    company_df.columns = ["Company", "Jobs"]
    fig_company = px.bar(
        company_df, x="Jobs", y="Company", orientation="h",
        color="Jobs", color_continuous_scale=["#1a1f2e", "#48BB78", "#38B2AC"],
        template="plotly_dark",
    )
    fig_company.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=0), height=350,
    )
    fig_company.update_yaxes(gridcolor="rgba(102,126,234,0.06)")
    fig_company.update_xaxes(gridcolor="rgba(102,126,234,0.06)")
    st.plotly_chart(fig_company, use_container_width=True)

# ── Role Distribution & Salary Distribution ──────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🎯 Role Distribution")
    cat_df = filtered["category"].value_counts().reset_index()
    cat_df.columns = ["Role", "Count"]
    fig_role = px.treemap(
        cat_df, path=["Role"], values="Count",
        color="Count",
        color_continuous_scale=["#1a1f2e", "#667EEA", "#764BA2"],
        template="plotly_dark",
    )
    fig_role.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=0, t=10, b=0), height=350,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_role, use_container_width=True)

with col4:
    st.markdown("#### 💵 Salary Distribution")
    fig_sal = px.histogram(
        filtered, x="salary_avg", nbins=50,
        color_discrete_sequence=["#667EEA"],
        template="plotly_dark",
        labels={"salary_avg": "Average Salary (USD)"},
    )
    fig_sal.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0), height=350,
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        yaxis=dict(gridcolor="rgba(102,126,234,0.06)", title="Count"),
    )
    st.plotly_chart(fig_sal, use_container_width=True)

# ── Seniority & Job Type ────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 📊 Seniority Breakdown")
    order = ["Junior", "Mid", "Senior", "Lead", "Principal"]
    sen_df = filtered["seniority"].value_counts().reindex(order).dropna().reset_index()
    sen_df.columns = ["Seniority", "Count"]
    fig_sen = px.bar(
        sen_df, x="Seniority", y="Count",
        color="Seniority",
        color_discrete_sequence=COLORS[:5],
        template="plotly_dark",
    )
    fig_sen.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0), height=300,
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig_sen, use_container_width=True)

with col6:
    st.markdown("#### 🏷️ Job Type Distribution")
    jt_df = filtered["job_type"].value_counts().reset_index()
    jt_df.columns = ["Type", "Count"]
    fig_jt = px.pie(
        jt_df, values="Count", names="Type",
        hole=0.5,
        color_discrete_sequence=COLORS,
        template="plotly_dark",
    )
    fig_jt.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=0, t=10, b=0), height=300,
    )
    st.plotly_chart(fig_jt, use_container_width=True)
