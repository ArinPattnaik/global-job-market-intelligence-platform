"""
Page 6: Salary Predictor
==========================
ML-powered salary prediction with interactive inputs and explanations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

st.set_page_config(page_title="Salary Predictor | GJMIP", page_icon="🤖", layout="wide")

with st.sidebar:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "processed" / "jobs_processed.csv"
    try:
        return pd.read_csv(path, parse_dates=["posted_date"])
    except FileNotFoundError:
        return pd.DataFrame()

@st.cache_resource
def train_model(df):
    """Train model and return bundle with encoders."""
    df = df.dropna(subset=["salary_avg"]).copy()
    df["skill_count"] = df["skills"].apply(
        lambda x: len(str(x).split(",")) if pd.notna(x) and x != "" else 0
    )

    le_country = LabelEncoder()
    le_category = LabelEncoder()
    le_seniority = LabelEncoder()

    df["country_enc"] = le_country.fit_transform(df["country_name"].astype(str))
    df["category_enc"] = le_category.fit_transform(df["category"].astype(str))
    df["seniority_enc"] = le_seniority.fit_transform(df["seniority"].astype(str))

    feature_cols = ["country_enc", "category_enc", "seniority_enc", "skill_count", "experience_years"]
    X = df[feature_cols]
    y = df["salary_avg"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "r2": round(r2_score(y_test, y_pred), 4),
        "mae": round(mean_absolute_error(y_test, y_pred), 2),
    }

    importances = dict(zip(
        ["Country", "Role Category", "Seniority", "Skill Count", "Experience Years"],
        model.feature_importances_.tolist()
    ))

    return {
        "model": model,
        "le_country": le_country,
        "le_category": le_category,
        "le_seniority": le_seniority,
        "metrics": metrics,
        "importances": importances,
    }


df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

bundle = train_model(df)
model = bundle["model"]

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">🤖 Salary Predictor</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        ML-powered salary estimation engine
    </span>
</div>
""", unsafe_allow_html=True)

# ── Model Performance ────────────────────────────────────────────────
st.markdown("")
mk1, mk2, mk3 = st.columns(3)
with mk1:
    st.metric("Model R² Score", f"{bundle['metrics']['r2']:.2%}")
with mk2:
    st.metric("Mean Absolute Error", f"${bundle['metrics']['mae']:,.0f}")
with mk3:
    st.metric("Training Samples", f"{len(df):,}")

st.markdown("")

# ── Prediction Interface ────────────────────────────────────────────
st.markdown("#### 🎯 Make a Prediction")

col_form, col_result = st.columns([2, 3])

with col_form:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.06) 0%, rgba(118,75,162,0.04) 100%);
                border: 1px solid rgba(102,126,234,0.12); border-radius: 16px;
                padding: 24px; margin-bottom: 16px;">
        <div style="font-weight: 600; color: #E6EDF3; margin-bottom: 16px; font-size: 1.05rem;">
            📋 Job Parameters
        </div>
    </div>
    """, unsafe_allow_html=True)

    pred_country = st.selectbox(
        "Country",
        sorted(bundle["le_country"].classes_),
        key="pred_country",
    )
    pred_category = st.selectbox(
        "Role Category",
        sorted(bundle["le_category"].classes_),
        key="pred_category",
    )
    pred_seniority = st.selectbox(
        "Seniority Level",
        ["Junior", "Mid", "Senior", "Lead", "Principal"],
        index=2,
        key="pred_seniority",
    )
    pred_skills = st.slider("Number of Skills", 1, 10, 5, key="pred_skills")
    pred_exp = st.slider("Years of Experience", 0, 25, 5, key="pred_exp")

    predict_btn = st.button("🚀 Predict Salary", use_container_width=True, type="primary")

with col_result:
    if predict_btn:
        try:
            country_enc = bundle["le_country"].transform([pred_country])[0]
            category_enc = bundle["le_category"].transform([pred_category])[0]
            seniority_enc = bundle["le_seniority"].transform([pred_seniority])[0]

            features = np.array([[country_enc, category_enc, seniority_enc, pred_skills, pred_exp]])
            prediction = model.predict(features)[0]

            # Confidence range (±15% as approximation)
            low = prediction * 0.85
            high = prediction * 1.15

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(72,187,120,0.08) 0%, rgba(56,178,172,0.08) 100%);
                        border: 1px solid rgba(72,187,120,0.2); border-radius: 16px;
                        padding: 32px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 0.85rem; color: #8B949E; text-transform: uppercase;
                            letter-spacing: 0.1em; margin-bottom: 8px;">Predicted Salary</div>
                <div style="font-size: 3rem; font-weight: 800;
                            background: linear-gradient(135deg, #48BB78 0%, #38B2AC 100%);
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                            background-clip: text;">
                    ${prediction:,.0f}
                </div>
                <div style="font-size: 0.9rem; color: #8B949E; margin-top: 4px;">
                    Range: ${low:,.0f} – ${high:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Details
            st.markdown(f"""
            <div style="background: rgba(102,126,234,0.04); border: 1px solid rgba(102,126,234,0.1);
                        border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                <div style="font-weight: 600; color: #E6EDF3; margin-bottom: 10px;">📝 Prediction Details</div>
                <div style="color: #8B949E; font-size: 0.88rem; line-height: 1.8;">
                    <strong style="color:#E6EDF3;">Country:</strong> {pred_country}<br>
                    <strong style="color:#E6EDF3;">Role:</strong> {pred_category}<br>
                    <strong style="color:#E6EDF3;">Seniority:</strong> {pred_seniority}<br>
                    <strong style="color:#E6EDF3;">Skills:</strong> {pred_skills} skills<br>
                    <strong style="color:#E6EDF3;">Experience:</strong> {pred_exp} years
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Country comparison
            st.markdown("##### 🌍 Same Role Across Countries")
            compare = []
            for c in bundle["le_country"].classes_:
                c_enc = bundle["le_country"].transform([c])[0]
                feat = np.array([[c_enc, category_enc, seniority_enc, pred_skills, pred_exp]])
                pred = model.predict(feat)[0]
                compare.append({"Country": c, "Predicted Salary": pred})

            comp_df = pd.DataFrame(compare).sort_values("Predicted Salary", ascending=False)
            fig_comp = px.bar(
                comp_df, x="Predicted Salary", y="Country", orientation="h",
                color="Predicted Salary",
                color_continuous_scale=["#1a1f2e", "#48BB78", "#38B2AC"],
                template="plotly_dark",
            )
            fig_comp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#E6EDF3"),
                showlegend=False, coloraxis_showscale=False,
                margin=dict(l=0, r=20, t=10, b=0), height=300,
                yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.markdown("""
        <div style="background: rgba(102,126,234,0.04); border: 1px solid rgba(102,126,234,0.1);
                    border-radius: 16px; padding: 40px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 12px;">🎯</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #E6EDF3; margin-bottom: 8px;">
                Configure & Predict
            </div>
            <div style="font-size: 0.9rem; color: #8B949E; line-height: 1.6;">
                Set your job parameters on the left and click<br>
                <strong style="color: #667EEA;">Predict Salary</strong> to get ML-powered estimation.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Feature Importances ─────────────────────────────────────────────
st.markdown("")
st.markdown("#### 📊 Model Feature Importances")

imp_df = pd.DataFrame([
    {"Feature": k, "Importance": v}
    for k, v in bundle["importances"].items()
]).sort_values("Importance", ascending=True)

fig_imp = px.bar(
    imp_df, x="Importance", y="Feature", orientation="h",
    color="Importance",
    color_continuous_scale=["#1a1f2e", "#667EEA", "#764BA2"],
    template="plotly_dark",
)
fig_imp.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#E6EDF3"),
    showlegend=False, coloraxis_showscale=False,
    margin=dict(l=0, r=20, t=10, b=0), height=250,
    yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
)
st.plotly_chart(fig_imp, use_container_width=True)
