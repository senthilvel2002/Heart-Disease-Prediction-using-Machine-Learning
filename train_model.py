import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
file_path = "heart_disease_dataset.csv"
df = pd.read_csv(file_path)

# Encode categorical variables
label_encoders = {}
categorical_cols = [
    'Gender', 'Smoking', 'Alcohol Intake', 'Family History', 
    'Diabetes', 'Obesity', 'Exercise Induced Angina', 'Chest Pain Type'
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Save encoders for future use

# Define features and target
X = df.drop(columns=['Heart Disease'])  # Features
y = df['Heart Disease']  # Target variable

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and preprocessing objects
joblib.dump(model, "saved_model.pkl")  # Save model
joblib.dump(scaler, "scaler.pkl")  # Save scaler
joblib.dump(label_encoders, "label_encoders.pkl")  # Save label encoders

print("✅ Model training complete. Saved model, scaler, and encoders.")
