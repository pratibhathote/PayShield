from backend.risk_engine import calculate_risk


transaction = {
    "amount": 48500,
    "hour": 2,
    "new_beneficiary": 1,
    "device_changed": 1,
    "location_changed": 1,
    "transactions_today": 2,
    "amount_deviation": 8.5,
    "beneficiary_age_days": 0,
    "is_weekend": 0,
}


result = calculate_risk(transaction)

print("\nPayShield Risk Analysis")
print("=" * 40)

print(f"Risk Score : {result['risk_score']}/100")
print(f"Risk Level : {result['risk_level']}")
print(f"Anomaly    : {result['is_anomaly']}")

print("\nReasons:")
for reason in result["reasons"]:
    print(f"- {reason}")

print("\nRecommendation:")
print(result["recommendation"])