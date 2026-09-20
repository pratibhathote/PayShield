import re


def analyze_message(message):
    """
    Analyze a payment-related message for common scam indicators.
    Educational/prototype use only.
    """

    text = message.lower()

    score = 0
    indicators = []

    # 1. Urgency / pressure
    urgency_words = [
        "urgent",
        "immediately",
        "hurry",
        "act now",
        "within 24 hours",
        "expires today",
        "last chance",
    ]

    if any(word in text for word in urgency_words):
        score += 20
        indicators.append("Urgency or pressure to act quickly")

    # 2. KYC / account verification
    kyc_words = [
        "kyc",
        "account blocked",
        "account suspended",
        "verify your account",
        "update kyc",
    ]

    if any(word in text for word in kyc_words):
        score += 20
        indicators.append("Account or KYC verification request")

    # 3. Sensitive information
    sensitive_words = [
        "otp",
        "pin",
        "password",
        "cvv",
        "card number",
        "upi pin",
    ]

    if any(word in text for word in sensitive_words):
        score += 25
        indicators.append("Request for sensitive financial credentials")

    # 4. Payment-related request
    payment_words = [
        "payment",
        "transfer",
        "pay",
        "refund",
        "fee",
        "charge",
        "cashback",
    ]

    if any(word in text for word in payment_words):
        score += 10
        indicators.append("Payment or money-related request")

    # 5. External links
    if re.search(r"https?://|www\.", text):
        score += 20
        indicators.append("External link detected")

    # 6. Rewards / prizes
    reward_words = [
        "winner",
        "won",
        "prize",
        "lottery",
        "reward",
        "cashback",
        "congratulations",
    ]

    if any(word in text for word in reward_words):
        score += 15
        indicators.append("Unexpected reward or prize claim")

    # 7. Contact pressure
    contact_words = [
        "call now",
        "contact immediately",
        "whatsapp",
        "customer care",
    ]

    if any(word in text for word in contact_words):
        score += 10
        indicators.append("Pressure to contact an external number/channel")

    # Keep score between 0 and 100
    score = min(score, 100)

    # Risk classification
    if score >= 60:
        risk_level = "HIGH"
        recommendation = (
            "Do not click links or share OTP, PIN, password, "
            "or banking credentials. Verify the message through "
            "the organisation's official channel."
        )

    elif score >= 30:
        risk_level = "MEDIUM"
        recommendation = (
            "Review the message carefully and verify the sender "
            "through an official channel before taking action."
        )

    else:
        risk_level = "LOW"
        recommendation = (
            "No major scam indicators detected. "
            "Still verify unexpected payment-related requests."
        )

    return {
        "risk_score": int(score),
        "risk_level": risk_level,
        "indicators": indicators,
        "recommendation": recommendation,
    }