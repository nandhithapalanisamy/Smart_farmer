import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier
)
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# =====================================================
# PATH CONFIGURATION
# =====================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SAVE_DIR = os.path.join(PROJECT_ROOT, "server", "models")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    os.path.join(DATA_DIR, "Cleaned_dataset.csv")
)

mapping = pd.read_csv(
    os.path.join(DATA_DIR, "Crop_label_mapping.csv")
)

crop_names = mapping.sort_values('Encoded_Value')['Crop'].tolist()
num_classes = len(crop_names)

# =====================================================
# FEATURES AND TARGET
# =====================================================

X = df.drop(columns=['label_encoded'])
y = df['label_encoded'].values

# =====================================================
# TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Train: {len(X_train)} | Test: {len(X_test)} | Classes: {num_classes}")

X_train_res, y_train_res = X_train, y_train

# =====================================================
# MODEL — EXTRA TREES (OPTIMIZED FOR SIZE & ACCURACY)
# =====================================================

print("Training Extra Trees...")
et = ExtraTreesClassifier(
    n_estimators=50,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
et.fit(X_train_res, y_train_res)
et_pred = et.predict(X_test)
et_acc  = accuracy_score(y_test, et_pred)
print(f"  Accuracy: {et_acc * 100:.2f}%")

# =====================================================
# RESULTS COMPARISON
# =====================================================

results = pd.DataFrame({
    "Model": [
        "Extra Trees",
    ],
    "Accuracy (%)": [
        round(et_acc  * 100, 2),
    ]
})

print("\n" + "=" * 45)
print("       INDIVIDUAL MODEL ACCURACY SCORES")
print("=" * 45)
for _, row in results.iterrows():
    print(f"  {row['Model']:<26}: {row['Accuracy (%)']:.2f}%")
print("=" * 45)

# =====================================================
# BEST MODEL REPORT
# =====================================================

best_row        = results.sort_values("Accuracy (%)", ascending=False).iloc[0]
best_model_name = best_row["Model"]
print(f"\nBest Model: {best_model_name} ({best_row['Accuracy (%)']:.2f}%)")

pred_map = {
    "Extra Trees":            et_pred,
}

print("\nClassification Report:")
print(classification_report(
    y_test,
    pred_map[best_model_name],
    target_names=crop_names
))

# =====================================================
# SAVE EXTRA TREES MODEL
# =====================================================

os.makedirs(SAVE_DIR, exist_ok=True)

# Save Extra Trees model with compression
model_path = os.path.join(SAVE_DIR, "crop_model.joblib")
joblib.dump(et, model_path, compress=9)

# Save feature names
feature_columns = X.columns.tolist()
joblib.dump(
    feature_columns,
    os.path.join(SAVE_DIR, "feature_columns.pkl")
)

# Save crop label mapping
joblib.dump(
    mapping,
    os.path.join(SAVE_DIR, "crop_mapping.pkl")
)

# Print model size
size_mb = os.path.getsize(model_path) / (1024 * 1024)

print("\n[OK] Extra Trees model saved successfully!")
print(f"Location: {SAVE_DIR}")
print(f"Model Size: {size_mb:.2f} MB")