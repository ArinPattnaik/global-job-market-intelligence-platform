"""
Global Job Market Intelligence Platform
=========================================
Main landing page with premium UI and global CSS injection.
"""

from __future__ import annotations

import streamlit as st
from pathlib import Path

# ── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Job Market Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ───────────────────────────────────────────────────────
st.markdown(
    (Path(__file__).parent / "assets" / "style.css").read_text()
    if (Path(__file__).parent / "assets" / "style.css").exists()
    else "",
    unsafe_allow_html=True,
)

# Inline fallback CSS (always applied)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

from utils.data_loader import load_processed_data

# ── Data Loading ─────────────────────────────────────────────────────
df = load_processed_data()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="font-size: 2.5rem; margin-bottom: 4px;">🌍</div>
        <div style="font-size: 1rem; font-weight: 700; color: #E6EDF3;
                    letter-spacing: 0.02em;">
            Job Market Intelligence
        </div>
        <div style="font-size: 0.75rem; color: #667EEA; font-weight: 500;
                    letter-spacing: 0.08em; text-transform: uppercase;">
            Analytics Platform v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="height:2px;background:linear-gradient(90deg,transparent,'
        '#667EEA,#764BA2,transparent);border:none;margin:16px 0;"></div>',
        unsafe_allow_html=True,
    )

    if not df.empty:
        st.markdown(f"""
        <div style="padding: 8px 0; text-align: center;">
            <span style="display:inline-block;padding:4px 12px;border-radius:20px;
                         font-size:0.75rem;font-weight:600;letter-spacing:0.05em;
                         text-transform:uppercase;background:rgba(72,187,120,0.15);
                         color:#48BB78;border:1px solid rgba(72,187,120,0.25);">
                ● LIVE
            </span>
            <span style="color: #8B949E; font-size: 0.8rem; margin-left: 8px;">
                {len(df):,} jobs tracked
            </span>
        </div>
        """, unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────────
st.markdown("")
st.markdown(
    '<div style="font-size:3.2rem;font-weight:800;line-height:1.1;'
    "background:linear-gradient(135deg,#667EEA 0%,#764BA2 50%,#48BB78 100%);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
    'background-clip:text;margin-bottom:8px;">'
    "Global Job Market<br>Intelligence Platform</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="font-size:1.2rem;color:#8B949E;font-weight:400;'
    'line-height:1.6;max-width:700px;">'
    "Real-time analytics across 5,000+ job postings, 8 countries, and "
    "80+ tracked skills. Powered by NLP-driven skill extraction and "
    "ML salary prediction.</div>",
    unsafe_allow_html=True,
)
st.markdown("")

# ── Hero KPIs ────────────────────────────────────────────────────────
if not df.empty:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Jobs", f"{len(df):,}")
    with c2:
        st.metric("Countries", f"{df['country_name'].nunique()}")
    with c3:
        avg_sal = df["salary_avg"].mean()
        st.metric("Avg Salary (USD)", f"${avg_sal:,.0f}")
    with c4:
        all_skills = df["skills"].dropna().str.split(",").explode().str.strip()
        all_skills = all_skills[all_skills != ""]
        top_skill = all_skills.value_counts().index[0] if len(all_skills) > 0 else "N/A"
        st.metric("Top Skill", top_skill.title())

    st.markdown(
        '<div style="height:2px;background:linear-gradient(90deg,transparent,'
        '#667EEA,#764BA2,transparent);border:none;margin:32px 0;"></div>',
        unsafe_allow_html=True,
    )

    # ── Feature Cards ────────────────────────────────────────────
    st.markdown("### ✨ Platform Features")
    st.markdown("")

    features = [
        ("📊", "Market Overview",
         "Interactive dashboards with KPIs, trend analysis, and hiring patterns."),
        ("🧠", "Skill Analytics",
         "NLP-powered extraction of 80+ in-demand skills with category breakdowns."),
        ("💰", "Salary Intelligence",
         "Deep salary analysis by country, role, seniority, and skill premium."),
        ("🌍", "Geographic Insights",
         "Country-level comparisons, city analytics, and regional hotspots."),
        ("🔎", "Job Explorer",
         "Advanced multi-filter search with styled job cards and CSV export."),
        ("🤖", "Salary Predictor",
         "ML-powered salary estimation with confidence intervals."),
        ("📤", "Upload & Analyze",
         "Upload any CSV/Excel dataset for automatic analysis."),
    ]

    _card_css = (
        "background:linear-gradient(135deg,rgba(102,126,234,0.06) 0%,"
        "rgba(118,75,162,0.04) 100%);border:1px solid rgba(102,126,234,0.12);"
        "border-radius:16px;padding:28px 24px;text-align:center;"
        "transition:all 0.3s cubic-bezier(0.4,0,0.2,1);height:100%;"
    )

    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(features[:4]):
        with cols[i]:
            st.markdown(
                f'<div style="{_card_css}">'
                f'<div style="font-size:2.5rem;margin-bottom:12px;">{icon}</div>'
                f'<div style="font-size:1.1rem;font-weight:700;color:#E6EDF3;'
                f'margin-bottom:8px;">{title}</div>'
                f'<div style="font-size:0.88rem;color:#8B949E;line-height:1.5;">'
                f"{desc}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("")
    cols2 = st.columns([1, 1, 1, 1])
    for i, (icon, title, desc) in enumerate(features[4:7]):
        with cols2[i]:
            st.markdown(
                f'<div style="{_card_css}">'
                f'<div style="font-size:2.5rem;margin-bottom:12px;">{icon}</div>'
                f'<div style="font-size:1.1rem;font-weight:700;color:#E6EDF3;'
                f'margin-bottom:8px;">{title}</div>'
                f'<div style="font-size:0.88rem;color:#8B949E;line-height:1.5;">'
                f"{desc}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="height:2px;background:linear-gradient(90deg,transparent,'
        '#667EEA,#764BA2,transparent);border:none;margin:32px 0;"></div>',
        unsafe_allow_html=True,
    )

    # ── Quick Stats ──────────────────────────────────────────────
    st.markdown("### 📈 Quick Snapshot")

    import plotly.express as px
    from config.settings import COLORS
    from utils.chart_helpers import apply_default_layout, GRADIENT_PURPLE

    c1, c2 = st.columns(2)
    with c1:
        country_counts = df["country_name"].value_counts().reset_index()
        country_counts.columns = ["Country", "Jobs"]
        fig = px.bar(
            country_counts, x="Jobs", y="Country", orientation="h",
            color="Jobs", color_continuous_scale=GRADIENT_PURPLE,
            template="plotly_dark",
        )
        apply_default_layout(
            fig, height=350, show_legend=False, coloraxis_showscale=False,
            title="Jobs by Country",
        )
        fig.update_layout(margin=dict(l=0, r=20, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["Role", "Count"]
        fig2 = px.pie(
            cat_counts, values="Count", names="Role",
            hole=0.55, color_discrete_sequence=COLORS,
            template="plotly_dark",
        )
        apply_default_layout(fig2, height=350, title="Role Distribution")
        fig2.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(font=dict(size=11)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        '<div style="text-align:center;color:#484F58;font-size:0.8rem;'
        'padding:20px 0;">👈 Use the sidebar to navigate through '
        "analytics pages</div>",
        unsafe_allow_html=True,
    )

else:
    st.warning(
        "No data found. Run `python data/generate_synthetic_data.py` "
        "to generate sample data."
    )
