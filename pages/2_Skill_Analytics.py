"""
Page 2: Skill Analytics
========================
NLP-powered skill demand analysis with category breakdowns and trends.
"""

from __future__ import annotations

from itertools import combinations

import pandas as pd
import plotly.express as px
import streamlit as st

from config.settings import CATEGORY_COLORS, COLORS, HEATMAP_SKILL_COUNT, TOP_SKILLS_COUNT
from nlp.skill_extraction import SKILL_TAXONOMY, get_skill_category
from utils.chart_helpers import HEATMAP_SCALE, apply_default_layout
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Skill Analytics", "🧠")

df = load_processed_data()
require_data(df)

page_header("🧠", "Skill Analytics", "NLP-powered skill demand intelligence")


# ── Parse Skills ─────────────────────────────────────────────────────
@st.cache_data
def parse_skills(dataframe: pd.DataFrame) -> pd.Series:
    series = dataframe["skills"].dropna().str.split(",").explode().str.strip()
    return series[series != ""]


# ── Filters ──────────────────────────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_countries = st.multiselect(
            "Country",
            sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique()),
            key="skill_countries",
        )
    with fc2:
        sel_categories = st.multiselect(
            "Skill Category",
            list(SKILL_TAXONOMY.keys()),
            default=list(SKILL_TAXONOMY.keys()),
            key="skill_cats",
        )

filtered = df[df["country_name"].isin(sel_countries)]
filtered_skills = parse_skills(filtered)
filtered_skills_cats = filtered_skills.apply(get_skill_category)
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
    st.markdown(f"#### 🏆 Top {TOP_SKILLS_COUNT} In-Demand Skills")
    top_skills = filtered_skills.value_counts().head(TOP_SKILLS_COUNT).reset_index()
    top_skills.columns = ["Skill", "Count"]
    top_skills["Category"] = top_skills["Skill"].apply(get_skill_category)

    fig = px.bar(
        top_skills, x="Count", y="Skill", orientation="h",
        color="Category", color_discrete_map=CATEGORY_COLORS,
        template="plotly_dark",
    )
    apply_default_layout(fig, height=600, legend_horizontal=True)
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 📂 Skills by Category")
    cat_counts = filtered_skills.apply(get_skill_category).value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig_cat = px.pie(
        cat_counts, values="Count", names="Category",
        hole=0.5, color="Category", color_discrete_map=CATEGORY_COLORS,
        template="plotly_dark",
    )
    apply_default_layout(fig_cat, height=350)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("#### 📊 Category Stats")
    cat_stats = cat_counts.copy()
    cat_stats["Percentage"] = (cat_stats["Count"] / cat_stats["Count"].sum() * 100).round(1)
    cat_stats["Percentage"] = cat_stats["Percentage"].astype(str) + "%"
    st.dataframe(cat_stats, use_container_width=True, hide_index=True)

# ── Skill x Country Heatmap ─────────────────────────────────────────
st.markdown("#### 🌡️ Skill Demand Heatmap by Country")

top_skill_names = filtered_skills.value_counts().head(HEATMAP_SKILL_COUNT).index.tolist()

heatmap_data = []
for _, row in filtered.iterrows():
    if pd.isna(row["skills"]):
        continue
    for s in (sk.strip() for sk in row["skills"].split(",")):
        if s in top_skill_names:
            heatmap_data.append({"skill": s, "country": row["country_name"]})

heatmap_df = pd.DataFrame(heatmap_data)
if not heatmap_df.empty:
    pivot = heatmap_df.groupby(["skill", "country"]).size().unstack(fill_value=0)
    fig_heat = px.imshow(
        pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        color_continuous_scale=HEATMAP_SCALE,
        template="plotly_dark", labels=dict(color="Job Count"), aspect="auto",
    )
    apply_default_layout(fig_heat, height=450)
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Skill Co-occurrence ──────────────────────────────────────────────
st.markdown("#### 🔗 Skill Co-occurrence (Top Pairs)")

from config.settings import COOCCURRENCE_PAIR_COUNT


@st.cache_data
def compute_cooccurrence(dataframe: pd.DataFrame, top_n: int = COOCCURRENCE_PAIR_COUNT):
    pair_counts: dict[tuple[str, str], int] = {}
    for skills_str in dataframe["skills"].dropna():
        skills = sorted({s.strip() for s in skills_str.split(",") if s.strip()})
        for a, b in combinations(skills, 2):
            key = (a, b)
            pair_counts[key] = pair_counts.get(key, 0) + 1
    pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return pd.DataFrame(
        [{"Skill A": a, "Skill B": b, "Co-occurrences": c} for (a, b), c in pairs]
    )


cooc = compute_cooccurrence(filtered)
if not cooc.empty:
    cooc["Pair"] = cooc["Skill A"] + " + " + cooc["Skill B"]
    fig_cooc = px.bar(
        cooc, x="Co-occurrences", y="Pair", orientation="h",
        color="Co-occurrences",
        color_continuous_scale=["#1a1f2e", "#48BB78", "#38B2AC"],
        template="plotly_dark",
    )
    apply_default_layout(
        fig_cooc, height=400, show_legend=False, coloraxis_showscale=False,
    )
    fig_cooc.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_cooc, use_container_width=True)
