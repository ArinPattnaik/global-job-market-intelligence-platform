"""
Global Job Market Intelligence Platform
=========================================
Main landing page with premium UI and global CSS injection.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# ── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Job Market Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Fonts ──────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Hide Streamlit Defaults ───────────────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ── Sidebar Styling ───────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #161B22 100%);
    border-right: 1px solid rgba(102, 126, 234, 0.15);
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #8B949E;
}

/* ── Metric Cards ──────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(102,126,234,0.08) 0%, rgba(118,75,162,0.08) 100%);
    border: 1px solid rgba(102,126,234,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(102,126,234,0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102,126,234,0.15);
}
div[data-testid="stMetric"] label {
    color: #8B949E !important;
    font-weight: 500;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 700;
    color: #E6EDF3 !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    font-size: 0.8rem;
}

/* ── Tabs ──────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    color: #8B949E;
    border-radius: 8px 8px 0 0;
    transition: all 0.2s ease;
}
button[data-baseweb="tab"]:hover {
    color: #667EEA;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #667EEA;
}

/* ── DataFrames ────────────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(102,126,234,0.15);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Expander ──────────────────────────────────────────── */
details {
    border: 1px solid rgba(102,126,234,0.12) !important;
    border-radius: 12px !important;
    background: rgba(102,126,234,0.03);
}

/* ── Selectbox / Multiselect ───────────────────────────── */
div[data-baseweb="select"] {
    border-radius: 8px;
}

/* ── Cards ─────────────────────────────────────────────── */
.glass-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.06) 0%, rgba(118,75,162,0.06) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(102,126,234,0.12);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(102,126,234,0.3);
    box-shadow: 0 8px 30px rgba(102,126,234,0.1);
}

/* ── Hero Section ──────────────────────────────────────── */
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #48BB78 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 1.2rem;
    color: #8B949E;
    font-weight: 400;
    line-height: 1.6;
    max-width: 700px;
}

/* ── Feature Cards ─────────────────────────────────────── */
.feature-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.06) 0%, rgba(118,75,162,0.04) 100%);
    border: 1px solid rgba(102,126,234,0.12);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}
.feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(102,126,234,0.35);
    box-shadow: 0 12px 40px rgba(102,126,234,0.12);
}
.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
}
.feature-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #E6EDF3;
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 0.88rem;
    color: #8B949E;
    line-height: 1.5;
}

/* ── Divider ───────────────────────────────────────────── */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #667EEA, #764BA2, transparent);
    border: none;
    margin: 32px 0;
    border-radius: 2px;
}

/* ── Badge ─────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-primary {
    background: rgba(102,126,234,0.15);
    color: #667EEA;
    border: 1px solid rgba(102,126,234,0.25);
}
.badge-success {
    background: rgba(72,187,120,0.15);
    color: #48BB78;
    border: 1px solid rgba(72,187,120,0.25);
}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0E1117;
}
::-webkit-scrollbar-thumb {
    background: #30363D;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #484F58;
}
</style>
""", unsafe_allow_html=True)


# ── Data Loading ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "data" / "processed" / "jobs_processed.csv"
    try:
        df = pd.read_csv(data_path, parse_dates=["posted_date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame()


df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="font-size: 2.5rem; margin-bottom: 4px;">🌍</div>
        <div style="font-size: 1rem; font-weight: 700; color: #E6EDF3; letter-spacing: 0.02em;">
            Job Market Intelligence
        </div>
        <div style="font-size: 0.75rem; color: #667EEA; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase;">
            Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    if not df.empty:
        st.markdown(f"""
        <div style="padding: 8px 0; text-align: center;">
            <span class="badge badge-success">● LIVE</span>
            <span style="color: #8B949E; font-size: 0.8rem; margin-left: 8px;">
                {len(df):,} jobs tracked
            </span>
        </div>
        """, unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────────
st.markdown("")
st.markdown('<div class="hero-title">Global Job Market<br>Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">'
    'Real-time analytics across 5,000+ job postings, 8 countries, and 80+ tracked skills. '
    'Powered by NLP-driven skill extraction and ML salary prediction.'
    '</div>',
    unsafe_allow_html=True
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
        all_skills = df["skills"].str.split(",").explode()
        top_skill = all_skills.value_counts().index[0] if len(all_skills) > 0 else "N/A"
        st.metric("Top Skill", top_skill.title())

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ── Feature Cards ────────────────────────────────────────────
    st.markdown("### ✨ Platform Features")
    st.markdown("")

    features = [
        ("📊", "Market Overview", "Interactive dashboards with KPIs, trend analysis, and hiring patterns across global markets."),
        ("🧠", "Skill Analytics", "NLP-powered extraction and analysis of 80+ in-demand skills with category breakdowns."),
        ("💰", "Salary Intelligence", "Deep salary analysis by country, role, seniority, and skill premium correlations."),
        ("🌍", "Geographic Insights", "Country-level comparisons, city analytics, and regional hiring hotspot identification."),
        ("🔎", "Job Explorer", "Advanced multi-filter search with styled job cards and detailed description views."),
        ("🤖", "Salary Predictor", "ML-powered salary estimation with confidence intervals and feature explanations."),
        ("📤", "Upload & Analyze", "Upload any CSV/Excel dataset for automatic analysis with smart visualizations."),
    ]

    # Row 1: 4 cards
    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(features[:4]):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # Row 2: 3 cards
    cols2 = st.columns([1, 1, 1, 1])
    for i, (icon, title, desc) in enumerate(features[4:7]):
        with cols2[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ── Quick Stats ──────────────────────────────────────────────
    st.markdown("### 📈 Quick Snapshot")

    c1, c2 = st.columns(2)
    with c1:
        import plotly.express as px
        country_counts = df["country_name"].value_counts().reset_index()
        country_counts.columns = ["Country", "Jobs"]
        fig = px.bar(
            country_counts, x="Jobs", y="Country", orientation="h",
            color="Jobs",
            color_continuous_scale=["#1a1f2e", "#667EEA", "#764BA2"],
            template="plotly_dark",
        )
        fig.update_layout(
            title="Jobs by Country",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#E6EDF3"),
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=20, t=40, b=0),
            height=350,
        )
        fig.update_yaxes(gridcolor="rgba(102,126,234,0.08)")
        fig.update_xaxes(gridcolor="rgba(102,126,234,0.08)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["Role", "Count"]
        colors = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
                  "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]
        fig2 = px.pie(
            cat_counts, values="Count", names="Role",
            hole=0.55,
            color_discrete_sequence=colors,
            template="plotly_dark",
        )
        fig2.update_layout(
            title="Role Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#E6EDF3"),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350,
            legend=dict(font=dict(size=11)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("")
    st.markdown(
        '<div style="text-align: center; color: #484F58; font-size: 0.8rem; padding: 20px 0;">'
        '👈 Use the sidebar to navigate through analytics pages'
        '</div>',
        unsafe_allow_html=True
    )

else:
    st.warning("No data found. Please run `python data/generate_synthetic_data.py` to generate sample data.")
