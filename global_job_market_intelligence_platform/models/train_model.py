
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/jobs_processed.csv")

df = df.dropna(subset=["salary_min"])

le_loc = LabelEncoder()
df["location_enc"] = le_loc.fit_transform(df["location"].astype(str))

X = df[["location_enc"]]
y = df["salary_min"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train,y_train)

joblib.dump(model,"models/salary_model.pkl")

print("Model trained")
