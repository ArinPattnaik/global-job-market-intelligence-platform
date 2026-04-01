
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging

logging.basicConfig(level=logging.INFO, filename="logs/train_model.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def train_model() -> None:
    """Train salary prediction model."""
    try:
        df = pd.read_csv("data/processed/jobs_processed.csv")
        df = df.dropna(subset=["salary_min"])
        le_loc = LabelEncoder()
        df["location_enc"] = le_loc.fit_transform(df["location"].astype(str))
        X = df[["location_enc"]]
        y = df["salary_min"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)
        joblib.dump(model, "models/salary_model.pkl")
        logger.info("Model trained")
    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise

if __name__ == "__main__":
    train_model()
