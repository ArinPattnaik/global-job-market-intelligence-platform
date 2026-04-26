"""
Tests for Salary Prediction Model
====================================
Validates model training, prediction, and metric quality.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from data.generate_synthetic_data import generate_jobs


@pytest.fixture(scope="module")
def training_data(tmp_path_factory) -> Path:
    """Generate and save a small dataset for model training tests."""
    tmp_dir = tmp_path_factory.mktemp("data")
    data_path = tmp_dir / "jobs_processed.csv"
    df = generate_jobs(n=300)
    df.to_csv(data_path, index=False)
    return data_path


class TestModelTraining:
    """Test the model training pipeline."""

    def test_train_returns_bundle(self, training_data: Path):
        from models.train_model import train_model

        bundle = train_model(data_path=training_data, save=False)

        assert "model" in bundle
        assert "le_country" in bundle
        assert "le_category" in bundle
        assert "le_seniority" in bundle
        assert "metrics" in bundle
        assert "importances" in bundle

    def test_metrics_reasonable(self, training_data: Path):
        from models.train_model import train_model

        bundle = train_model(data_path=training_data, save=False)
        metrics = bundle["metrics"]

        # R² should be positive (model better than mean)
        assert metrics["r2_score"] > 0.0
        # MAE should be reasonable (not astronomically high)
        assert metrics["mae"] < 100_000
        # RMSE should exist
        assert metrics["rmse"] > 0

    def test_model_can_predict(self, training_data: Path):
        from models.train_model import train_model

        bundle = train_model(data_path=training_data, save=False)
        model = bundle["model"]

        # Create a sample feature vector
        features = np.array([[0, 0, 2, 5, 5]])
        prediction = model.predict(features)

        assert len(prediction) == 1
        assert prediction[0] > 0

    def test_feature_importances_sum_to_one(self, training_data: Path):
        from models.train_model import train_model

        bundle = train_model(data_path=training_data, save=False)
        total = sum(bundle["importances"].values())
        assert abs(total - 1.0) < 0.01
