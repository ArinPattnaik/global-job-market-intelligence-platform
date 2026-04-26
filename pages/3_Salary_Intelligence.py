"""
Page 3: Salary Intelligence
=============================
Deep salary analysis by country, role, seniority, and skill premium.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.settings import COLORS, SENIORITY_ORDER
from utils.chart_helpers import (
    GRADIENT_PURPLE,
    GRADIENT_WARM,
    apply_default_layout,
    format_currency,
)
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Salary Intelligence", "💰")

df = load_processed_data()
require_data(df)

page_header("💰", "Salary Intelligence", "Compensation analytics and insights")

# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_countries = st.multiselect(
            "Country",
            sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
            key="sal_countries",
        )
    with fc2:
        sel_seniorities = st.multiselect(
            "Seniority",
            sorted(df["seniority"].unique()),
            default=sorted(df["seniority"].unique()),
            key="sal_seniority",
        )

filtered = df[
    df["country_name"].isin(sel_countries) & df["seniority"].isin(sel_seniorities)
]

if filtered.empty:
    st.info("No data matches filters.")
    st.stop()

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Median Salary", format_currency(filtered["salary_avg"].median()))
with k2:
    st.metric("Mean Salary", format_currency(filtered["salary_avg"].mean()))
with k3:
    st.metric("Min Salary", format_currency(filtered["salary_min"].min()))
with k4:
    st.metric("Max Salary", format_currency(filtered["salary_max"].max()))
with k5:
    p90 = filtered["salary_avg"].quantile(0.9)
    st.metric("90th Percentile", format_currency(p90))

st.markdown("")

# ── Salary by Country & Role ────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 Salary by Country")
    fig_box = px.box(
        filtered, x="country_name", y="salary_avg",
        color="country_name", color_discrete_sequence=COLORS,
        template="plotly_dark",
        labels={"salary_avg": "Average Salary (USD)", "country_name": "Country"},
    )
    apply_default_layout(fig_box, height=400, show_legend=False)
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.markdown("#### 🎯 Salary by Role")
    fig_role = px.box(
        filtered, x="category", y="salary_avg",
        color="category", color_discrete_sequence=COLORS,
        template="plotly_dark",
        labels={"salary_avg": "Average Salary (USD)", "category": "Role"},
    )
    apply_default_layout(fig_role, height=400, show_legend=False)
    fig_role.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_role, use_container_width=True)

# ── Salary by Seniority ─────────────────────────────────────────────
st.markdown("#### 📊 Salary by Seniority Level")
sen_sal = (
    filtered.groupby("seniority")["salary_avg"]
    .agg(["mean", "median", "min", "max"])
    .reindex(SENIORITY_ORDER)
    .dropna()
    .reset_index()
)
sen_sal.columns = ["Seniority", "Mean", "Median", "Min", "Max"]

fig_sen = go.Figure()
fig_sen.add_trace(go.Bar(
    x=sen_sal["Seniority"], y=sen_sal["Mean"],
    name="Mean", marker_color="#667EEA",
    hovertemplate="<b>%{x}</b><br>Mean: $%{y:,.0f}<extra></extra>",
))
fig_sen.add_trace(go.Bar(
    x=sen_sal["Seniority"], y=sen_sal["Median"],
    name="Median", marker_color="#764BA2",
    hovertemplate="<b>%{x}</b><br>Median: $%{y:,.0f}<extra></extra>",
))
apply_default_layout(fig_sen, height=350, legend_horizontal=True)
fig_sen.update_layout(barmode="group")
fig_sen.update_yaxes(title="USD")
st.plotly_chart(fig_sen, use_container_width=True)

# ── Skill Premium & Top Companies ────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 💎 Top Paying Skills")
    skill_salary = []
    for _, row in filtered.iterrows():
        if pd.isna(row["skills"]):
            continue
        for s in row["skills"].split(","):
            s = s.strip()
            if s:
                skill_salary.append({"skill": s, "salary": row["salary_avg"]})

    if skill_salary:
        ss_df = pd.DataFrame(skill_salary)
        avg_salary = filtered["salary_avg"].mean()
        skill_avg = ss_df.groupby("skill")["salary"].mean().reset_index()
        skill_avg.columns = ["Skill", "Avg Salary"]
        skill_avg["Premium"] = (
            (skill_avg["Avg Salary"] - avg_salary) / avg_salary * 100
        ).round(1)
        skill_avg = skill_avg.sort_values("Avg Salary", ascending=False).head(15)

        fig_premium = px.bar(
            skill_avg, x="Avg Salary", y="Skill", orientation="h",
            color="Premium",
            color_continuous_scale=["#E53E3E", "#D69E2E", "#48BB78"],
            template="plotly_dark",
            labels={"Avg Salary": "Average Salary (USD)"},
        )
        apply_default_layout(fig_premium, height=450)
        fig_premium.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_premium, use_container_width=True)

with col4:
    st.markdown("#### 🏢 Top Paying Companies")
    comp_sal = (
        filtered.groupby("company")["salary_avg"]
        .agg(["mean", "count"])
        .reset_index()
    )
    comp_sal.columns = ["Company", "Avg Salary", "Jobs"]
    comp_sal = (
        comp_sal[comp_sal["Jobs"] >= 5]
        .sort_values("Avg Salary", ascending=False)
        .head(15)
    )

    fig_comp = px.bar(
        comp_sal, x="Avg Salary", y="Company", orientation="h",
        color="Avg Salary", color_continuous_scale=GRADIENT_WARM,
        template="plotly_dark", hover_data=["Jobs"],
    )
    apply_default_layout(
        fig_comp, height=450, show_legend=False, coloraxis_showscale=False,
    )
    fig_comp.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_comp, use_container_width=True)

# ── Salary Distribution ─────────────────────────────────────────────
st.markdown("#### 📈 Salary Distribution with Percentiles")
fig_dist = px.histogram(
    filtered, x="salary_avg", nbins=60,
    color_discrete_sequence=["#667EEA"],
    template="plotly_dark",
    labels={"salary_avg": "Average Salary (USD)"},
    marginal="box",
)
for pct, color, name in [(25, "#48BB78", "P25"), (50, "#ED8936", "P50"), (75, "#E53E3E", "P75")]:
    val = filtered["salary_avg"].quantile(pct / 100)
    fig_dist.add_vline(
        x=val, line_dash="dash", line_color=color,
        annotation_text=f"{name}: ${val:,.0f}",
        annotation_font_color=color,
    )
apply_default_layout(fig_dist, height=380, show_legend=False)
fig_dist.update_yaxes(title="Count")
st.plotly_chart(fig_dist, use_container_width=True)
