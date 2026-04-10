"""
Page 3: Salary Intelligence
=============================
Deep salary analysis by country, role, seniority, and skill premium.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Salary Intelligence | GJMIP", page_icon="💰", layout="wide")

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

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
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">💰 Salary Intelligence</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        Compensation analytics and insights
    </span>
</div>
""", unsafe_allow_html=True)

# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_countries = st.multiselect(
            "Country", sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
            key="sal_countries",
        )
    with fc2:
        sel_seniorities = st.multiselect(
            "Seniority", sorted(df["seniority"].unique()),
            default=sorted(df["seniority"].unique()),
            key="sal_seniority",
        )

filtered = df[df["country_name"].isin(sel_countries) & df["seniority"].isin(sel_seniorities)]

if filtered.empty:
    st.info("No data matches filters.")
    st.stop()

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Median Salary", f"${filtered['salary_avg'].median():,.0f}")
with k2:
    st.metric("Mean Salary", f"${filtered['salary_avg'].mean():,.0f}")
with k3:
    st.metric("Min Salary", f"${filtered['salary_min'].min():,.0f}")
with k4:
    st.metric("Max Salary", f"${filtered['salary_max'].max():,.0f}")
with k5:
    p90 = filtered['salary_avg'].quantile(0.9)
    st.metric("90th Percentile", f"${p90:,.0f}")

st.markdown("")

# ── Salary by Country ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 Salary by Country")
    fig_box = px.box(
        filtered, x="country_name", y="salary_avg",
        color="country_name",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
        labels={"salary_avg": "Average Salary (USD)", "country_name": "Country"},
    )
    fig_box.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0), height=400,
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.markdown("#### 🎯 Salary by Role")
    fig_role = px.box(
        filtered, x="category", y="salary_avg",
        color="category",
        color_discrete_sequence=COLORS,
        template="plotly_dark",
        labels={"salary_avg": "Average Salary (USD)", "category": "Role"},
    )
    fig_role.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0), height=400,
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)", tickangle=-45),
        yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig_role, use_container_width=True)

# ── Salary by Seniority ─────────────────────────────────────────────
st.markdown("#### 📊 Salary by Seniority Level")
order = ["Junior", "Mid", "Senior", "Lead", "Principal"]
sen_sal = filtered.groupby("seniority")["salary_avg"].agg(["mean", "median", "min", "max"]).reindex(order).dropna()
sen_sal = sen_sal.reset_index()
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
fig_sen.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E6EDF3"),
    margin=dict(l=0, r=0, t=10, b=0), height=350,
    barmode="group",
    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    yaxis=dict(gridcolor="rgba(102,126,234,0.06)", title="USD"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
)
st.plotly_chart(fig_sen, use_container_width=True)

# ── Skill Premium Analysis ──────────────────────────────────────────
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
        skill_avg["Premium"] = ((skill_avg["Avg Salary"] - avg_salary) / avg_salary * 100).round(1)
        skill_avg = skill_avg.sort_values("Avg Salary", ascending=False).head(15)

        fig_premium = px.bar(
            skill_avg, x="Avg Salary", y="Skill", orientation="h",
            color="Premium",
            color_continuous_scale=["#E53E3E", "#D69E2E", "#48BB78"],
            template="plotly_dark",
            labels={"Avg Salary": "Average Salary (USD)"},
        )
        fig_premium.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#E6EDF3"),
            coloraxis_showscale=True,
            margin=dict(l=0, r=20, t=10, b=0), height=450,
            yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
            xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
        )
        st.plotly_chart(fig_premium, use_container_width=True)

with col4:
    st.markdown("#### 🏢 Top Paying Companies")
    comp_sal = filtered.groupby("company")["salary_avg"].agg(["mean", "count"]).reset_index()
    comp_sal.columns = ["Company", "Avg Salary", "Jobs"]
    comp_sal = comp_sal[comp_sal["Jobs"] >= 5].sort_values("Avg Salary", ascending=False).head(15)

    fig_comp = px.bar(
        comp_sal, x="Avg Salary", y="Company", orientation="h",
        color="Avg Salary",
        color_continuous_scale=["#1a1f2e", "#D69E2E", "#ED8936"],
        template="plotly_dark",
        hover_data=["Jobs"],
    )
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=0), height=450,
        yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ── Salary Distribution with Percentiles ─────────────────────────────
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
    fig_dist.add_vline(x=val, line_dash="dash", line_color=color,
                       annotation_text=f"{name}: ${val:,.0f}", annotation_font_color=color)
fig_dist.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E6EDF3"),
    showlegend=False,
    margin=dict(l=0, r=0, t=10, b=0), height=380,
    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    yaxis=dict(gridcolor="rgba(102,126,234,0.06)", title="Count"),
)
st.plotly_chart(fig_dist, use_container_width=True)
