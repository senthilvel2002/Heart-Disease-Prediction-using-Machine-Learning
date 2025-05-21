import joblib

# Load label encoders
label_encoders = joblib.load("label_encoders.pkl")

# Print available keys
print("Available keys in label_encoders:", label_encoders.keys())
