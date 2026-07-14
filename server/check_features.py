import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
feature_columns_path = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

feature_columns = joblib.load(feature_columns_path)

for col in feature_columns:
    print(col)