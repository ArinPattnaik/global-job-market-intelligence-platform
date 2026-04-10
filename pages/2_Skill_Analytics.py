"""
Page 2: Skill Analytics
========================
NLP-powered skill demand analysis with category breakdowns and trends.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp.skill_extraction import SKILL_TAXONOMY, get_skill_category

st.set_page_config(page_title="Skill Analytics | GJMIP", page_icon="🧠", layout="wide")

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

CATEGORY_COLORS = {
    "Programming": "#667EEA",
    "Data & Databases": "#764BA2",
    "Big Data": "#48BB78",
    "Cloud & Infrastructure": "#ED8936",
    "ML & AI": "#E53E3E",
    "BI & Visualization": "#38B2AC",
    "Analytics & Statistics": "#D69E2E",
    "DevOps & Tools": "#9F7AEA",
    "Soft Skills": "#FC8181",
}

@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "processed" / "jobs_processed.csv"
    try:
        df = pd.read_csv(path, parse_dates=["posted_date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">🧠 Skill Analytics</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        NLP-powered skill demand intelligence
    </span>
</div>
""", unsafe_allow_html=True)

# ── Parse Skills ─────────────────────────────────────────────────────
@st.cache_data
def parse_skills(df):
    skills_series = df["skills"].dropna().str.split(",").explode().str.strip()
    skills_series = skills_series[skills_series != ""]
    return skills_series

all_skills = parse_skills(df)

# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_countries = st.multiselect(
            "Country", sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
            key="skill_countries",
        )
    with fc2:
        sel_categories = st.multiselect(
            "Skill Category", list(SKILL_TAXONOMY.keys()),
            default=list(SKILL_TAXONOMY.keys()),
            key="skill_cats",
        )

filtered = df[df["country_name"].isin(sel_countries)]
filtered_skills = filtered["skills"].dropna().str.split(",").explode().str.strip()
filtered_skills = filtered_skills[filtered_skills != ""]
filtered_skills_cats = filtered_skills.apply(get_skill_category)

# Filter by selected categories
mask = filtered_skills_cats.isin(sel_categories)
filtered_skills = filtered_skills[mask]

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown("")
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Unique Skills", f"{filtered_skills.nunique()}")
with k2:
    st.metric("Skill Mentions", f"{len(filtered_skills):,}")
with k3:
    top = filtered_skills.value_counts().index[0] if len(filtered_skills) > 0 else "N/A"
    st.metric("Most In-Demand", top.title())
with k4:
    avg_per_job = filtered["skills"].dropna().apply(lambda x: len(x.split(","))).mean()
    st.metric("Avg Skills/Job", f"{avg_per_job:.1f}")

st.markdown("")

# ── Top Skills Bar Chart ────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("#### 🏆 Top 25 In-Demand Skills")
    top_skills = filtered_skills.value_counts().head(25).reset_index()
    top_skills.columns = ["Skill", "Count"]
    top_skills["Category"] = top_skills["Skill"].apply(get_skill_category)

    fig = px.bar(
        top_skills, x="Count", y="Skill", orientation="h",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        template="plotly_dark",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=20, t=10, b=0), height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10)),
        yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 📂 Skills by Category")
    cat_counts = filtered_skills.apply(get_skill_category).value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig_cat = px.pie(
        cat_counts, values="Count", names="Category",
        hole=0.5,
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        template="plotly_dark",
    )
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=0, t=10, b=0), height=350,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # ── Skill Stats Table ────────────────────────────────────────
    st.markdown("#### 📊 Category Stats")
    cat_stats = cat_counts.copy()
    cat_stats["Percentage"] = (cat_stats["Count"] / cat_stats["Count"].sum() * 100).round(1)
    cat_stats["Percentage"] = cat_stats["Percentage"].astype(str) + "%"
    st.dataframe(cat_stats, use_container_width=True, hide_index=True)

# ── Skill x Country Heatmap ─────────────────────────────────────────
st.markdown("#### 🌡️ Skill Demand Heatmap by Country")

top_N = 15
top_skill_names = filtered_skills.value_counts().head(top_N).index.tolist()

heatmap_data = []
for _, row in filtered.iterrows():
    if pd.isna(row["skills"]):
        continue
    job_skills = [s.strip() for s in row["skills"].split(",")]
    for s in job_skills:
        if s in top_skill_names:
            heatmap_data.append({"skill": s, "country": row["country_name"]})

heatmap_df = pd.DataFrame(heatmap_data)
if not heatmap_df.empty:
    pivot = heatmap_df.groupby(["skill", "country"]).size().unstack(fill_value=0)
    fig_heat = px.imshow(
        pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        color_continuous_scale=["#0E1117", "#667EEA", "#764BA2"],
        template="plotly_dark",
        labels=dict(color="Job Count"),
        aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        margin=dict(l=0, r=0, t=10, b=0), height=450,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Skill Co-occurrence ──────────────────────────────────────────────
st.markdown("#### 🔗 Skill Co-occurrence (Top Pairs)")

from itertools import combinations

@st.cache_data
def compute_cooccurrence(df, top_n=15):
    pair_counts = {}
    for skills_str in df["skills"].dropna():
        skills = sorted(set(s.strip() for s in skills_str.split(",") if s.strip()))
        for a, b in combinations(skills, 2):
            key = (a, b)
            pair_counts[key] = pair_counts.get(key, 0) + 1
    pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return pd.DataFrame([
        {"Skill A": a, "Skill B": b, "Co-occurrences": c}
        for (a, b), c in pairs
    ])

cooc = compute_cooccurrence(filtered)
if not cooc.empty:
    cooc["Pair"] = cooc["Skill A"] + " + " + cooc["Skill B"]
    fig_cooc = px.bar(
        cooc, x="Co-occurrences", y="Pair", orientation="h",
        color="Co-occurrences",
        color_continuous_scale=["#1a1f2e", "#48BB78", "#38B2AC"],
        template="plotly_dark",
    )
    fig_cooc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E6EDF3"),
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=0), height=400,
        yaxis=dict(autorange="reversed", gridcolor="rgba(102,126,234,0.06)"),
        xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    )
    st.plotly_chart(fig_cooc, use_container_width=True)
