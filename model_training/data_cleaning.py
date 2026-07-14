import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    os.path.join(DATA_DIR, "crop_recommendation_dataset_v3.csv")
)

print("Original Shape:", df.shape)

# =====================================================
# BASIC CHECKS
# =====================================================

print("\nMissing Values:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)

# =====================================================
# HANDLE MISSING VALUES
# =====================================================

for col in df.select_dtypes(include=np.number).columns:
    df[col].fillna(df[col].median(), inplace=True)

for col in df.select_dtypes(include='object').columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# =====================================================
# OUTLIER TREATMENT (IQR CAPPING)
# =====================================================

feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall']

for col in feature_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = np.clip(df[col], lower, upper)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

df['Total_NPK']        = df['N'] + df['P'] + df['K']
df['Avg_NPK']          = df['Total_NPK'] / 3
df['NPK_Ratio']        = df['N'] / (df['P'] + df['K'] + 1)
df['N_P_ratio']        = df['N'] / (df['P'] + 1)
df['P_K_ratio']        = df['P'] / (df['K'] + 1)
df['Temp_Humidity']    = df['temperature'] * df['humidity']
df['Rainfall_Temp']    = df['rainfall'] / (df['temperature'] + 1)
df['pH_rainfall']      = df['pH'] * df['rainfall']
df['N_rainfall']       = df['N'] * df['rainfall']
df['K_humidity']       = df['K'] * df['humidity']

# =====================================================
# ENCODE CATEGORY (ONE-HOT — nominal feature)
# =====================================================

cat_dummies = pd.get_dummies(df['category'], prefix='cat', dtype=int)
df = pd.concat([df.drop(columns=['category']), cat_dummies], axis=1)

# =====================================================
# NOTE: Scaling removed because tree-based models (like ExtraTrees)
# are scale-invariant, and removing scaling avoids mismatched
# scaling bugs in production when predicting on raw input data.
# =====================================================

# =====================================================
# ENCODE TARGET LABEL (integer — for model training)
# =====================================================

label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['label'])

# Save mapping so you can decode predictions later
mapping = pd.DataFrame({
    "Crop":          label_encoder.classes_,
    "Encoded_Value": range(len(label_encoder.classes_))
})
mapping.to_csv(
    os.path.join(DATA_DIR, "Crop_label_mapping.csv"),
    index=False
)

# Drop original string label
df = df.drop(columns=['label'])

# =====================================================
# SAVE CLEANED DATASET
# =====================================================

df.to_csv(
    os.path.join(DATA_DIR, "Cleaned_dataset.csv"),
    index=False
)

print("\nProcessed Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nData Cleaned Successfully!")