"""
Multi-Feature Salary Prediction Model
=======================================
Uses country, role category, seniority, and skill count to predict salary.
Includes model evaluation and metadata export.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def train_model() -> dict:
    """
    Train a multi-feature salary prediction model.
    Returns dict with model, encoders, and evaluation metrics.
    """
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "processed" / "jobs_processed.csv"
    model_path = base_dir / "models" / "salary_model.pkl"
    meta_path = base_dir / "models" / "model_metadata.json"

    try:
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["salary_avg"])

        # ── Feature Engineering ──────────────────────────────────
        df["skill_count"] = df["skills"].apply(
            lambda x: len(str(x).split(",")) if pd.notna(x) and x != "" else 0
        )

        # Encode categoricals
        le_country = LabelEncoder()
        le_category = LabelEncoder()
        le_seniority = LabelEncoder()

        df["country_enc"] = le_country.fit_transform(df["country"].astype(str))
        df["category_enc"] = le_category.fit_transform(df["category"].astype(str))
        df["seniority_enc"] = le_seniority.fit_transform(df["seniority"].astype(str))

        feature_cols = ["country_enc", "category_enc", "seniority_enc",
                        "skill_count", "experience_years"]
        X = df[feature_cols]
        y = df["salary_avg"]

        # ── Train/Test Split ─────────────────────────────────────
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # ── Model Training ───────────────────────────────────────
        model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
        )
        model.fit(X_train, y_train)

        # ── Evaluation ───────────────────────────────────────────
        y_pred = model.predict(X_test)
        metrics = {
            "r2_score": round(r2_score(y_test, y_pred), 4),
            "mae": round(mean_absolute_error(y_test, y_pred), 2),
            "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
        }

        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")
        metrics["cv_r2_mean"] = round(cv_scores.mean(), 4)
        metrics["cv_r2_std"] = round(cv_scores.std(), 4)

        # Feature importances
        importances = dict(zip(feature_cols, model.feature_importances_.tolist()))

        # ── Save Model & Metadata ────────────────────────────────
        model_bundle = {
            "model": model,
            "le_country": le_country,
            "le_category": le_category,
            "le_seniority": le_seniority,
            "feature_cols": feature_cols,
            "metrics": metrics,
            "importances": importances,
        }
        joblib.dump(model_bundle, model_path)

        metadata = {
            "features": feature_cols,
            "metrics": metrics,
            "importances": importances,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "countries": le_country.classes_.tolist(),
            "categories": le_category.classes_.tolist(),
            "seniorities": le_seniority.classes_.tolist(),
        }
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Model trained — R²={metrics['r2_score']}, MAE=${metrics['mae']:,.0f}")
        return model_bundle

    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise


if __name__ == "__main__":
    result = train_model()
    print(f"\nModel Performance:")
    for k, v in result["metrics"].items():
        print(f"  {k}: {v}")
    print(f"\nFeature Importances:")
    for k, v in result["importances"].items():
        print(f"  {k}: {v:.4f}")
