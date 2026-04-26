"""
Multi-Feature Salary Prediction Model
=======================================
Uses country, role category, seniority, and skill count to predict salary.
Includes model evaluation, cross-validation, and metadata export.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

from config.logging_config import get_logger
from config.settings import (
    MODEL_CV_FOLDS,
    MODEL_LEARNING_RATE,
    MODEL_MAX_DEPTH,
    MODEL_META_PATH,
    MODEL_N_ESTIMATORS,
    MODEL_PATH,
    MODEL_RANDOM_STATE,
    MODEL_TEST_SIZE,
    PROCESSED_DATA_PATH,
)

logger = get_logger("train_model")

FEATURE_COLS = [
    "country_enc",
    "category_enc",
    "seniority_enc",
    "skill_count",
    "experience_years",
]

FEATURE_DISPLAY_NAMES = {
    "country_enc": "Country",
    "category_enc": "Role Category",
    "seniority_enc": "Seniority",
    "skill_count": "Skill Count",
    "experience_years": "Experience Years",
}


def _compute_skill_count(skills_col: pd.Series) -> pd.Series:
    """Derive skill count from the comma-separated skills column."""
    return skills_col.apply(
        lambda x: len(str(x).split(",")) if pd.notna(x) and str(x).strip() else 0
    )


def train_model(
    data_path: Path | None = None,
    save: bool = True,
) -> dict[str, Any]:
    """
    Train a multi-feature salary prediction model.

    Parameters
    ----------
    data_path : Path, optional
        Override the default processed data path.
    save : bool
        Whether to persist the model and metadata to disk.

    Returns
    -------
    dict with model, encoders, metrics, and feature importances.
    """
    data_path = data_path or PROCESSED_DATA_PATH

    try:
        df = pd.read_csv(data_path)
        df = df.dropna(subset=["salary_avg"])
        logger.info("Training on %d samples from %s", len(df), data_path.name)

        # ── Feature Engineering ──────────────────────────────────
        df["skill_count"] = _compute_skill_count(df["skills"])

        le_country = LabelEncoder()
        le_category = LabelEncoder()
        le_seniority = LabelEncoder()

        df["country_enc"] = le_country.fit_transform(df["country"].astype(str))
        df["category_enc"] = le_category.fit_transform(df["category"].astype(str))
        df["seniority_enc"] = le_seniority.fit_transform(df["seniority"].astype(str))

        X = df[FEATURE_COLS]
        y = df["salary_avg"]

        # ── Train / Test Split ───────────────────────────────────
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=MODEL_TEST_SIZE,
            random_state=MODEL_RANDOM_STATE,
        )

        # ── Model Training ───────────────────────────────────────
        model = GradientBoostingRegressor(
            n_estimators=MODEL_N_ESTIMATORS,
            max_depth=MODEL_MAX_DEPTH,
            learning_rate=MODEL_LEARNING_RATE,
            random_state=MODEL_RANDOM_STATE,
        )
        model.fit(X_train, y_train)

        # ── Evaluation ───────────────────────────────────────────
        y_pred = model.predict(X_test)
        metrics: dict[str, float] = {
            "r2_score": round(r2_score(y_test, y_pred), 4),
            "mae": round(mean_absolute_error(y_test, y_pred), 2),
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 2),
        }

        cv_scores = cross_val_score(
            model,
            X,
            y,
            cv=MODEL_CV_FOLDS,
            scoring="r2",
        )
        metrics["cv_r2_mean"] = round(float(cv_scores.mean()), 4)
        metrics["cv_r2_std"] = round(float(cv_scores.std()), 4)

        importances = dict(zip(FEATURE_COLS, model.feature_importances_.tolist(), strict=False))

        bundle: dict[str, Any] = {
            "model": model,
            "le_country": le_country,
            "le_category": le_category,
            "le_seniority": le_seniority,
            "feature_cols": FEATURE_COLS,
            "metrics": metrics,
            "importances": importances,
        }

        # ── Persist ──────────────────────────────────────────────
        if save:
            joblib.dump(bundle, MODEL_PATH)
            metadata = {
                "features": FEATURE_COLS,
                "metrics": metrics,
                "importances": importances,
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "countries": le_country.classes_.tolist(),
                "categories": le_category.classes_.tolist(),
                "seniorities": le_seniority.classes_.tolist(),
            }
            MODEL_META_PATH.write_text(json.dumps(metadata, indent=2))
            logger.info("Model saved → %s", MODEL_PATH)

        logger.info(
            "Model trained — R²=%.4f, MAE=$%.0f, RMSE=$%.0f",
            metrics["r2_score"],
            metrics["mae"],
            metrics["rmse"],
        )
        return bundle

    except FileNotFoundError:
        logger.error("Data file not found: %s", data_path)
        raise
    except Exception:
        logger.exception("Error training model")
        raise


if __name__ == "__main__":
    result = train_model()
    print("\nModel Performance:")
    for k, v in result["metrics"].items():
        print(f"  {k}: {v}")
    print("\nFeature Importances:")
    for k, v in result["importances"].items():
        name = FEATURE_DISPLAY_NAMES.get(k, k)
        print(f"  {name}: {v:.4f}")
