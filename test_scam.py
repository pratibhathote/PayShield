from backend.scam_analyzer import analyze_message


message = """
URGENT! Your bank account will be blocked today.
Complete your KYC immediately using this link:
https://example.com/verify
"""


result = analyze_message(message)

print("\nPayShield Scam Message Analysis")
print("=" * 40)

print(f"Risk Score : {result['risk_score']}/100")
print(f"Risk Level : {result['risk_level']}")

print("\nIndicators:")
for indicator in result["indicators"]:
    print(f"- {indicator}")

print("\nRecommendation:")
print(result["recommendation"])