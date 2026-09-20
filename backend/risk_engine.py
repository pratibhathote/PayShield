import joblib
import pandas as pd


MODEL_PATH = "models/risk_model.pkl"

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


# Load trained model once
model = joblib.load(MODEL_PATH)


def calculate_risk(transaction):
    """
    Analyze a transaction and return:
    - risk score
    - risk level
    - reasons
    - recommendation
    """

    # Convert input into DataFrame
    df = pd.DataFrame([transaction])

    # Make prediction
    prediction = model.predict(df[FEATURES])[0]

    # ---------------------------------------------------------
    # Base risk score
    # ---------------------------------------------------------

    if prediction == -1:
        risk_score = 60
    else:
        risk_score = 15

    reasons = []

    # ---------------------------------------------------------
    # Behavioral risk factors
    # ---------------------------------------------------------

    if transaction["amount"] >= 25000:
        risk_score += 15
        reasons.append("High transaction amount")

    elif transaction["amount"] >= 10000:
        risk_score += 7
        reasons.append("Transaction amount is above typical range")

    # Unusual hour
    if transaction["hour"] <= 5 or transaction["hour"] >= 23:
        risk_score += 10
        reasons.append("Unusual transaction hour")

    # New beneficiary
    if transaction["new_beneficiary"] == 1:
        risk_score += 10
        reasons.append("New beneficiary detected")

    # Device change
    if transaction["device_changed"] == 1:
        risk_score += 10
        reasons.append("Device change detected")

    # Location change
    if transaction["location_changed"] == 1:
        risk_score += 10
        reasons.append("Location change detected")

    # High transaction frequency
    if transaction["transactions_today"] >= 10:
        risk_score += 8
        reasons.append("High transaction frequency today")

    # Amount deviation
    if transaction["amount_deviation"] >= 5:
        risk_score += 12
        reasons.append("Transaction amount is significantly different from usual")

    elif transaction["amount_deviation"] >= 3:
        risk_score += 7
        reasons.append("Transaction amount differs from usual behavior")

    # New beneficiary age
    if transaction["beneficiary_age_days"] == 0:
        if "New beneficiary detected" not in reasons:
            reasons.append("Beneficiary has no transaction history")

    # Weekend
    if transaction["is_weekend"] == 1:
        # Weekend alone isn't highly suspicious,
        # so we don't add a large score.
        pass

    # ---------------------------------------------------------
    # Keep score between 0 and 100
    # ---------------------------------------------------------

    risk_score = min(risk_score, 100)

    # ---------------------------------------------------------
    # Risk level
    # ---------------------------------------------------------

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # ---------------------------------------------------------
    # Recommendation
    # ---------------------------------------------------------

    if risk_level == "HIGH":
        recommendation = (
            "Pause the payment and verify the recipient "
            "through a trusted channel before proceeding."
        )

    elif risk_level == "MEDIUM":
        recommendation = (
            "Review the transaction details and verify the "
            "recipient before proceeding."
        )

    else:
        recommendation = (
            "No major risk indicators detected. "
            "Review the payment details before confirming."
        )

    return {
        "risk_score":int(risk_score),
        "risk_level": risk_level,
        "is_anomaly": bool(prediction == -1),
        "reasons": reasons,
        "recommendation": recommendation,
    }