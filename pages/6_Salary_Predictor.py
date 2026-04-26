"""
Page 6: Salary Predictor
==========================
ML-powered salary prediction with interactive inputs and explanations.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from config.settings import (
    MODEL_LEARNING_RATE,
    MODEL_MAX_DEPTH,
    MODEL_N_ESTIMATORS,
    MODEL_RANDOM_STATE,
    MODEL_TEST_SIZE,
    SENIORITY_ORDER,
)
from utils.chart_helpers import GRADIENT_GREEN, GRADIENT_PURPLE, apply_default_layout
from utils.data_loader import load_processed_data, require_data
from utils.ui_components import page_header, setup_page

setup_page("Salary Predictor", "🤖")


@st.cache_resource
def train_model(df: pd.DataFrame) -> dict:
    """Train model and return bundle with encoders."""
    df = df.dropna(subset=["salary_avg"]).copy()
    df["skill_count"] = df["skills"].apply(
        lambda x: len(str(x).split(",")) if pd.notna(x) and str(x).strip() else 0
    )

    le_country = LabelEncoder()
    le_category = LabelEncoder()
    le_seniority = LabelEncoder()

    df["country_enc"] = le_country.fit_transform(df["country_name"].astype(str))
    df["category_enc"] = le_category.fit_transform(df["category"].astype(str))
    df["seniority_enc"] = le_seniority.fit_transform(df["seniority"].astype(str))

    feature_cols = [
        "country_enc",
        "category_enc",
        "seniority_enc",
        "skill_count",
        "experience_years",
    ]
    X = df[feature_cols]
    y = df["salary_avg"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=MODEL_TEST_SIZE,
        random_state=MODEL_RANDOM_STATE,
    )

    model = GradientBoostingRegressor(
        n_estimators=MODEL_N_ESTIMATORS,
        max_depth=MODEL_MAX_DEPTH,
        learning_rate=MODEL_LEARNING_RATE,
        random_state=MODEL_RANDOM_STATE,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Compute residual-based confidence interval
    residuals = y_test.values - y_pred
    residual_std = float(np.std(residuals))

    return {
        "model": model,
        "le_country": le_country,
        "le_category": le_category,
        "le_seniority": le_seniority,
        "metrics": {
            "r2": round(r2_score(y_test, y_pred), 4),
            "mae": round(mean_absolute_error(y_test, y_pred), 2),
        },
        "importances": dict(
            zip(
                ["Country", "Role Category", "Seniority", "Skill Count", "Experience Years"],
                model.feature_importances_.tolist(),
                strict=False,
            )
        ),
        "residual_std": residual_std,
    }


df = load_processed_data()
require_data(df)

bundle = train_model(df)
model = bundle["model"]

page_header("🤖", "Salary Predictor", "ML-powered salary estimation engine")

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
    st.markdown(
        """
    <div style="background:linear-gradient(135deg,rgba(102,126,234,0.06) 0%,
                rgba(118,75,162,0.04) 100%);border:1px solid rgba(102,126,234,0.12);
                border-radius:16px;padding:24px;margin-bottom:16px;">
        <div style="font-weight:600;color:#E6EDF3;margin-bottom:16px;font-size:1.05rem;">
            📋 Job Parameters</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

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
        SENIORITY_ORDER,
        index=2,
        key="pred_seniority",
    )
    pred_skills = st.slider("Number of Skills", 1, 10, 5, key="pred_skills")
    pred_exp = st.slider("Years of Experience", 0, 25, 5, key="pred_exp")

    predict_btn = st.button(
        "🚀 Predict Salary",
        use_container_width=True,
        type="primary",
    )

with col_result:
    if predict_btn:
        try:
            country_enc = bundle["le_country"].transform([pred_country])[0]
            category_enc = bundle["le_category"].transform([pred_category])[0]
            seniority_enc = bundle["le_seniority"].transform([pred_seniority])[0]

            features = np.array(
                [
                    [
                        country_enc,
                        category_enc,
                        seniority_enc,
                        pred_skills,
                        pred_exp,
                    ]
                ]
            )
            prediction = model.predict(features)[0]

            # Data-driven confidence interval (1.96 * std ≈ 95% CI)
            margin = 1.96 * bundle["residual_std"]
            low = max(0, prediction - margin)
            high = prediction + margin

            st.markdown(
                f"""
            <div style="background:linear-gradient(135deg,rgba(72,187,120,0.08) 0%,
                        rgba(56,178,172,0.08) 100%);border:1px solid rgba(72,187,120,0.2);
                        border-radius:16px;padding:32px;text-align:center;margin-bottom:20px;">
                <div style="font-size:0.85rem;color:#8B949E;text-transform:uppercase;
                            letter-spacing:0.1em;margin-bottom:8px;">Predicted Salary</div>
                <div style="font-size:3rem;font-weight:800;
                            background:linear-gradient(135deg,#48BB78 0%,#38B2AC 100%);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                            background-clip:text;">
                    ${prediction:,.0f}</div>
                <div style="font-size:0.9rem;color:#8B949E;margin-top:4px;">
                    95% CI: ${low:,.0f} – ${high:,.0f}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
            <div style="background:rgba(102,126,234,0.04);border:1px solid rgba(102,126,234,0.1);
                        border-radius:12px;padding:16px;margin-bottom:16px;">
                <div style="font-weight:600;color:#E6EDF3;margin-bottom:10px;">📝 Prediction Details</div>
                <div style="color:#8B949E;font-size:0.88rem;line-height:1.8;">
                    <strong style="color:#E6EDF3;">Country:</strong> {pred_country}<br>
                    <strong style="color:#E6EDF3;">Role:</strong> {pred_category}<br>
                    <strong style="color:#E6EDF3;">Seniority:</strong> {pred_seniority}<br>
                    <strong style="color:#E6EDF3;">Skills:</strong> {pred_skills} skills<br>
                    <strong style="color:#E6EDF3;">Experience:</strong> {pred_exp} years
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Country comparison
            st.markdown("##### 🌍 Same Role Across Countries")
            compare = []
            for c in bundle["le_country"].classes_:
                c_enc = bundle["le_country"].transform([c])[0]
                feat = np.array([[c_enc, category_enc, seniority_enc, pred_skills, pred_exp]])
                compare.append({"Country": c, "Predicted Salary": model.predict(feat)[0]})

            comp_df = pd.DataFrame(compare).sort_values("Predicted Salary", ascending=False)
            fig_comp = px.bar(
                comp_df,
                x="Predicted Salary",
                y="Country",
                orientation="h",
                color="Predicted Salary",
                color_continuous_scale=GRADIENT_GREEN,
                template="plotly_dark",
            )
            apply_default_layout(
                fig_comp,
                height=300,
                show_legend=False,
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.markdown(
            """
        <div style="background:rgba(102,126,234,0.04);border:1px solid rgba(102,126,234,0.1);
                    border-radius:16px;padding:40px;text-align:center;">
            <div style="font-size:3rem;margin-bottom:12px;">🎯</div>
            <div style="font-size:1.1rem;font-weight:600;color:#E6EDF3;margin-bottom:8px;">
                Configure & Predict</div>
            <div style="font-size:0.9rem;color:#8B949E;line-height:1.6;">
                Set your job parameters on the left and click<br>
                <strong style="color:#667EEA;">Predict Salary</strong> to get ML-powered estimation.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ── Feature Importances ─────────────────────────────────────────────
st.markdown("")
st.markdown("#### 📊 Model Feature Importances")

imp_df = pd.DataFrame(
    [{"Feature": k, "Importance": v} for k, v in bundle["importances"].items()]
).sort_values("Importance", ascending=True)

fig_imp = px.bar(
    imp_df,
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    color_continuous_scale=GRADIENT_PURPLE,
    template="plotly_dark",
)
apply_default_layout(
    fig_imp,
    height=250,
    show_legend=False,
    coloraxis_showscale=False,
)
st.plotly_chart(fig_imp, use_container_width=True)
