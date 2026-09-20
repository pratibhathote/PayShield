import os
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DATA_PATH = "data/transactions.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

print("Loading transaction dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded: {len(df)} transactions")


# ---------------------------------------------------------
# Features used by the anomaly detector
# ---------------------------------------------------------

FEATURES = [
    "amount",
    "hour",
    "new_beneficiary",
    "device_changed",
    "location_changed",
    "transactions_today",
    "amount_deviation",
    "beneficiary_age_days",
    "is_weekend",
]

X = df[FEATURES]


# ---------------------------------------------------------
# Build ML pipeline
# ---------------------------------------------------------

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "isolation_forest",
        IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42,
            n_jobs=-1
        )
    )
])


# ---------------------------------------------------------
# Train model
# ---------------------------------------------------------

print("Training Isolation Forest...")

model.fit(X)

print("Model training completed!")


# ---------------------------------------------------------
# Create models directory
# ---------------------------------------------------------

os.makedirs(MODEL_DIR, exist_ok=True)


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------

joblib.dump(
    model,
    MODEL_PATH
)

print(f"Model saved to: {MODEL_PATH}")


# ---------------------------------------------------------
# Test predictions
# ---------------------------------------------------------

predictions = model.predict(X)

anomalies = (predictions == -1).sum()
normal = (predictions == 1).sum()

print("\nModel summary:")
print(f"Normal transactions   : {normal}")
print(f"Anomalous transactions: {anomalies}")
print(f"Total transactions    : {len(predictions)}")

print("\nTraining complete!")