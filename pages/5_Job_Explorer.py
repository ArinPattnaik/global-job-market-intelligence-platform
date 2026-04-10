"""
Page 5: Job Explorer
======================
Advanced multi-filter job search with styled cards.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Job Explorer | GJMIP", page_icon="🔎", layout="wide")

with st.sidebar:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")

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
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">🔎 Job Explorer</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        Search, filter, and explore job listings
    </span>
</div>
""", unsafe_allow_html=True)

# ── Search & Filters ────────────────────────────────────────────────
st.markdown("")

c1, c2 = st.columns([3, 1])
with c1:
    search_query = st.text_input(
        "🔍 Search job titles, companies, or skills",
        placeholder="e.g., Senior Data Scientist, Python, Google...",
    )
with c2:
    sort_by = st.selectbox("Sort by", ["Most Recent", "Highest Salary", "Lowest Salary", "Company A-Z"])

with st.expander("🎛️ Advanced Filters", expanded=True):
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_countries = st.multiselect(
            "Country", sorted(df["country_name"].unique()),
            default=[],
            key="je_countries",
        )
    with fc2:
        sel_categories = st.multiselect(
            "Role Category", sorted(df["category"].unique()),
            default=[],
            key="je_categories",
        )
    with fc3:
        sel_seniorities = st.multiselect(
            "Seniority", sorted(df["seniority"].unique()),
            default=[],
            key="je_seniority",
        )
    with fc4:
        sel_job_types = st.multiselect(
            "Job Type", sorted(df["job_type"].unique()),
            default=[],
            key="je_jobtypes",
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
        skill_search = st.text_input("Skills (comma-separated)", placeholder="python, sql, aws")

# ── Apply Filters ────────────────────────────────────────────────────
results = df.copy()

if search_query:
    q = search_query.lower()
    results = results[
        results["title"].str.lower().str.contains(q, na=False) |
        results["company"].str.lower().str.contains(q, na=False) |
        results["skills"].str.lower().str.contains(q, na=False)
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
    (results["salary_avg"] >= salary_range[0]) &
    (results["salary_avg"] <= salary_range[1])
]

if skill_search:
    for skill in skill_search.split(","):
        skill = skill.strip().lower()
        if skill:
            results = results[results["skills"].str.lower().str.contains(skill, na=False)]

# Sort
if sort_by == "Most Recent":
    results = results.sort_values("posted_date", ascending=False)
elif sort_by == "Highest Salary":
    results = results.sort_values("salary_avg", ascending=False)
elif sort_by == "Lowest Salary":
    results = results.sort_values("salary_avg", ascending=True)
elif sort_by == "Company A-Z":
    results = results.sort_values("company")

# ── Results Header ───────────────────────────────────────────────────
st.markdown("")
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
    <span style="font-size: 0.95rem; color: #8B949E;">
        Showing <strong style="color: #667EEA;">{min(len(results), 50)}</strong> of
        <strong style="color: #E6EDF3;">{len(results):,}</strong> matching jobs
    </span>
</div>
""", unsafe_allow_html=True)

if results.empty:
    st.info("No jobs match your search criteria. Try adjusting your filters.")
    st.stop()

# ── Job Cards ────────────────────────────────────────────────────────
JOB_TYPE_COLORS = {
    "Full-time": "#48BB78", "Remote": "#667EEA", "Contract": "#ED8936",
    "Hybrid": "#9F7AEA", "Part-time": "#D69E2E",
}

SENIORITY_COLORS = {
    "Junior": "#4FD1C5", "Mid": "#48BB78", "Senior": "#667EEA",
    "Lead": "#764BA2", "Principal": "#ED8936",
}

for idx, row in results.head(50).iterrows():
    jt_color = JOB_TYPE_COLORS.get(row["job_type"], "#8B949E")
    sen_color = SENIORITY_COLORS.get(row["seniority"], "#8B949E")
    skills_html = ""
    if pd.notna(row["skills"]):
        skills_list = [s.strip() for s in row["skills"].split(",") if s.strip()]
        skills_html = " ".join([
            f'<span style="display:inline-block; padding:2px 8px; margin:2px; '
            f'border-radius:12px; font-size:0.72rem; font-weight:500; '
            f'background:rgba(102,126,234,0.12); color:#667EEA; '
            f'border:1px solid rgba(102,126,234,0.2);">{s}</span>'
            for s in skills_list
        ])

    posted = pd.to_datetime(row["posted_date"]).strftime("%b %d, %Y") if pd.notna(row["posted_date"]) else ""

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.04) 0%, rgba(118,75,162,0.03) 100%);
                border: 1px solid rgba(102,126,234,0.10); border-radius: 14px;
                padding: 20px 24px; margin-bottom: 12px;
                transition: all 0.3s ease;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #E6EDF3; margin-bottom: 4px;">
                    {row['title']}
                </div>
                <div style="font-size: 0.9rem; color: #8B949E; margin-bottom: 8px;">
                    🏢 {row['company']} &nbsp;·&nbsp; 📍 {row['location']} &nbsp;·&nbsp; 📅 {posted}
                </div>
                <div style="margin-bottom: 8px;">
                    <span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.72rem;
                           font-weight:600; background:rgba({int(jt_color[1:3],16)},{int(jt_color[3:5],16)},{int(jt_color[5:7],16)},0.15);
                           color:{jt_color}; border:1px solid {jt_color}30; margin-right:6px;">
                        {row['job_type']}
                    </span>
                    <span style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.72rem;
                           font-weight:600; background:rgba({int(sen_color[1:3],16)},{int(sen_color[3:5],16)},{int(sen_color[5:7],16)},0.15);
                           color:{sen_color}; border:1px solid {sen_color}30;">
                        {row['seniority']}
                    </span>
                </div>
                <div>{skills_html}</div>
            </div>
            <div style="text-align: right; min-width: 150px;">
                <div style="font-size: 1.3rem; font-weight: 700; color: #48BB78;">
                    ${row['salary_avg']:,.0f}
                </div>
                <div style="font-size: 0.75rem; color: #8B949E;">
                    ${row['salary_min']:,.0f} – ${row['salary_max']:,.0f}
                </div>
                <div style="font-size: 0.75rem; color: #8B949E; margin-top: 4px;">
                    {row['experience_years']} yrs exp.
                </div>
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
    st.markdown(f"""
    <div style="padding: 8px 0; color: #8B949E; font-size: 0.8rem;">
        {len(results):,} total results available
    </div>
    """, unsafe_allow_html=True)
