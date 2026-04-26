"""
Page 5: Job Explorer
======================
Advanced multi-filter job search with styled cards and export.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.settings import JOB_EXPLORER_PAGE_SIZE, JOB_TYPE_COLORS, SENIORITY_COLORS
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Job Explorer", "🔎")

df = load_processed_data()
require_data(df)

page_header("🔎", "Job Explorer", "Search, filter, and explore job listings")

# ── Search & Filters ────────────────────────────────────────────────
st.markdown("")
c1, c2 = st.columns([3, 1])
with c1:
    search_query = st.text_input(
        "🔍 Search job titles, companies, or skills",
        placeholder="e.g., Senior Data Scientist, Python, Google…",
    )
with c2:
    sort_by = st.selectbox(
        "Sort by",
        ["Most Recent", "Highest Salary", "Lowest Salary", "Company A-Z"],
    )

with st.expander("🎛️ Advanced Filters", expanded=True):
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_countries = st.multiselect(
            "Country", sorted(df["country_name"].unique()), key="je_countries",
        )
    with fc2:
        sel_categories = st.multiselect(
            "Role Category", sorted(df["category"].unique()), key="je_categories",
        )
    with fc3:
        sel_seniorities = st.multiselect(
            "Seniority", sorted(df["seniority"].unique()), key="je_seniority",
        )
    with fc4:
        sel_job_types = st.multiselect(
            "Job Type", sorted(df["job_type"].unique()), key="je_jobtypes",
        )

    fc5, fc6 = st.columns(2)
    with fc5:
        salary_range = st.slider(
            "Salary Range (USD)",
            min_value=int(df["salary_min"].min()),
            max_value=int(df["salary_max"].max()),
            value=(int(df["salary_min"].min()), int(df["salary_max"].max())),
            step=5000,
            format="$%d",
        )
    with fc6:
        skill_search = st.text_input(
            "Skills (comma-separated)", placeholder="python, sql, aws",
        )

# ── Apply Filters ────────────────────────────────────────────────────
results = df.copy()

if search_query:
    q = search_query.lower()
    results = results[
        results["title"].str.lower().str.contains(q, na=False, regex=False)
        | results["company"].str.lower().str.contains(q, na=False, regex=False)
        | results["skills"].str.lower().str.contains(q, na=False, regex=False)
    ]

if sel_countries:
    results = results[results["country_name"].isin(sel_countries)]
if sel_categories:
    results = results[results["category"].isin(sel_categories)]
if sel_seniorities:
    results = results[results["seniority"].isin(sel_seniorities)]
if sel_job_types:
    results = results[results["job_type"].isin(sel_job_types)]

results = results[
    (results["salary_avg"] >= salary_range[0])
    & (results["salary_avg"] <= salary_range[1])
]

if skill_search:
    for skill in skill_search.split(","):
        skill = skill.strip().lower()
        if skill:
            results = results[
                results["skills"].str.lower().str.contains(skill, na=False, regex=False)
            ]

# Sort
sort_map = {
    "Most Recent": ("posted_date", False),
    "Highest Salary": ("salary_avg", False),
    "Lowest Salary": ("salary_avg", True),
    "Company A-Z": ("company", True),
}
sort_col, sort_asc = sort_map[sort_by]
results = results.sort_values(sort_col, ascending=sort_asc)

# ── Results Header ───────────────────────────────────────────────────
st.markdown("")
display_count = min(len(results), JOB_EXPLORER_PAGE_SIZE)
st.markdown(
    f'<div style="font-size:0.95rem;color:#8B949E;margin-bottom:16px;">'
    f'Showing <strong style="color:#667EEA;">{display_count}</strong> of '
    f'<strong style="color:#E6EDF3;">{len(results):,}</strong> matching jobs</div>',
    unsafe_allow_html=True,
)

if results.empty:
    st.info("No jobs match your search criteria. Try adjusting your filters.")
    st.stop()

# ── Job Cards ────────────────────────────────────────────────────────
def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"


for _, row in results.head(JOB_EXPLORER_PAGE_SIZE).iterrows():
    jt_color = JOB_TYPE_COLORS.get(row["job_type"], "#8B949E")
    sen_color = SENIORITY_COLORS.get(row["seniority"], "#8B949E")

    skills_html = ""
    if pd.notna(row["skills"]):
        skills_list = [s.strip() for s in row["skills"].split(",") if s.strip()]
        skills_html = " ".join(
            f'<span style="display:inline-block;padding:2px 8px;margin:2px;'
            f"border-radius:12px;font-size:0.72rem;font-weight:500;"
            f"background:rgba(102,126,234,0.12);color:#667EEA;"
            f'border:1px solid rgba(102,126,234,0.2);">{s}</span>'
            for s in skills_list
        )

    posted = (
        pd.to_datetime(row["posted_date"]).strftime("%b %d, %Y")
        if pd.notna(row["posted_date"])
        else ""
    )

    jt_rgb = _hex_to_rgb(jt_color)
    sen_rgb = _hex_to_rgb(sen_color)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(102,126,234,0.04) 0%,
                rgba(118,75,162,0.03) 100%);border:1px solid rgba(102,126,234,0.10);
                border-radius:14px;padding:20px 24px;margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;">
            <div style="flex:1;min-width:300px;">
                <div style="font-size:1.1rem;font-weight:700;color:#E6EDF3;margin-bottom:4px;">
                    {row['title']}</div>
                <div style="font-size:0.9rem;color:#8B949E;margin-bottom:8px;">
                    🏢 {row['company']} · 📍 {row['location']} · 📅 {posted}</div>
                <div style="margin-bottom:8px;">
                    <span style="display:inline-block;padding:3px 10px;border-radius:12px;
                           font-size:0.72rem;font-weight:600;
                           background:rgba({jt_rgb},0.15);color:{jt_color};
                           border:1px solid {jt_color}30;margin-right:6px;">
                        {row['job_type']}</span>
                    <span style="display:inline-block;padding:3px 10px;border-radius:12px;
                           font-size:0.72rem;font-weight:600;
                           background:rgba({sen_rgb},0.15);color:{sen_color};
                           border:1px solid {sen_color}30;">
                        {row['seniority']}</span>
                </div>
                <div>{skills_html}</div>
            </div>
            <div style="text-align:right;min-width:150px;">
                <div style="font-size:1.3rem;font-weight:700;color:#48BB78;">
                    ${row['salary_avg']:,.0f}</div>
                <div style="font-size:0.75rem;color:#8B949E;">
                    ${row['salary_min']:,.0f} – ${row['salary_max']:,.0f}</div>
                <div style="font-size:0.75rem;color:#8B949E;margin-top:4px;">
                    {row['experience_years']} yrs exp.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Export ────────────────────────────────────────────────────────────
st.markdown("")
col_exp1, col_exp2, _ = st.columns([1, 1, 4])
with col_exp1:
    csv = results.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name="job_search_results.csv",
        mime="text/csv",
    )
with col_exp2:
    st.markdown(
        f'<div style="padding:8px 0;color:#8B949E;font-size:0.8rem;">'
        f"{len(results):,} total results available</div>",
        unsafe_allow_html=True,
    )
