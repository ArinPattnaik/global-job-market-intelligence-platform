"""
Page 1: Market Overview Dashboard
===================================
Interactive dashboard with KPIs, trends, and hiring analytics.
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from config.settings import COLORS, SENIORITY_ORDER
from utils.chart_helpers import (
    GRADIENT_PURPLE,
    apply_default_layout,
    format_currency,
)
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Market Overview", "📊")

df = load_processed_data()
require_data(df)

page_header("📊", "Market Overview", "Global hiring trends and market analytics")

# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sel_countries = st.multiselect(
            "Country",
            sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
            key="mo_countries",
        )
    with fc2:
        sel_categories = st.multiselect(
            "Role Category",
            sorted(df["category"].unique()),
            default=sorted(df["category"].unique()),
            key="mo_categories",
        )
    with fc3:
        sel_seniorities = st.multiselect(
            "Seniority",
            sorted(df["seniority"].unique()),
            default=sorted(df["seniority"].unique()),
            key="mo_seniority",
        )

filtered = df[
    df["country_name"].isin(sel_countries)
    & df["category"].isin(sel_categories)
    & df["seniority"].isin(sel_seniorities)
]

if filtered.empty:
    st.info("No data matches the selected filters.")
    st.stop()

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Total Jobs", f"{len(filtered):,}")
with k2:
    st.metric("Companies", f"{filtered['company'].nunique()}")
with k3:
    st.metric("Avg Salary", format_currency(filtered["salary_avg"].mean()))
with k4:
    st.metric("Countries", f"{filtered['country_name'].nunique()}")
with k5:
    remote_pct = (filtered["job_type"] == "Remote").sum() / len(filtered) * 100
    st.metric("Remote %", f"{remote_pct:.1f}%")

st.markdown("")

# ── Hiring Trends ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Monthly Hiring Trend")
    monthly = filtered.set_index("posted_date").resample("M")["job_id"].count().reset_index()
    monthly.columns = ["Month", "Jobs"]
    fig_trend = px.area(
        monthly,
        x="Month",
        y="Jobs",
        color_discrete_sequence=["#667EEA"],
        template="plotly_dark",
    )
    fig_trend.update_traces(fillcolor="rgba(102,126,234,0.1)")
    apply_default_layout(fig_trend, height=350, show_legend=False)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("#### 🏢 Top 15 Hiring Companies")
    top_companies = filtered["company"].value_counts().head(15).reset_index()
    top_companies.columns = ["Company", "Jobs"]
    fig_comp = px.bar(
        top_companies,
        x="Jobs",
        y="Company",
        orientation="h",
        color="Jobs",
        color_continuous_scale=GRADIENT_PURPLE,
        template="plotly_dark",
    )
    apply_default_layout(
        fig_comp,
        height=350,
        show_legend=False,
        coloraxis_showscale=False,
    )
    fig_comp.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_comp, use_container_width=True)

# ── Country & Role Breakdown ────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🌍 Jobs by Country")
    country_counts = filtered["country_name"].value_counts().reset_index()
    country_counts.columns = ["Country", "Jobs"]
    fig_country = px.pie(
        country_counts,
        values="Jobs",
        names="Country",
        hole=0.5,
        color_discrete_sequence=COLORS,
        template="plotly_dark",
    )
    apply_default_layout(fig_country, height=350)
    st.plotly_chart(fig_country, use_container_width=True)

with col4:
    st.markdown("#### 🎯 Jobs by Role")
    role_counts = filtered["category"].value_counts().reset_index()
    role_counts.columns = ["Role", "Jobs"]
    fig_role = px.bar(
        role_counts,
        x="Jobs",
        y="Role",
        orientation="h",
        color="Role",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
    )
    apply_default_layout(fig_role, height=350, show_legend=False)
    fig_role.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_role, use_container_width=True)

# ── Seniority Distribution ──────────────────────────────────────────
st.markdown("#### 📊 Seniority Distribution")
sen_counts = filtered["seniority"].value_counts().reindex(SENIORITY_ORDER).dropna().reset_index()
sen_counts.columns = ["Seniority", "Count"]
fig_sen = px.bar(
    sen_counts,
    x="Seniority",
    y="Count",
    color="Seniority",
    color_discrete_sequence=COLORS,
    template="plotly_dark",
)
apply_default_layout(fig_sen, height=300, show_legend=False)
st.plotly_chart(fig_sen, use_container_width=True)
