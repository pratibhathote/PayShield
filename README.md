# 🛡️ PayShield — AI Pre-Payment Risk & Scam Analyzer

> **Think before you pay.**

PayShield is an AI-assisted **pre-payment risk analysis system** designed to help users identify potentially suspicious payment scenarios **before completing a transaction**.

Instead of claiming to detect fraud after it happens, PayShield focuses on analyzing **transaction behavior and scam-message indicators** and presenting an explainable risk assessment to the user.

---

## 🚨 Problem

Digital payment scams often rely on users making quick decisions under pressure.

Common warning signs include:

- Unexpected payment requests
- New or unfamiliar beneficiaries
- Unusual transaction amounts
- Device or location changes
- Unusual transaction timing
- Suspicious payment-related messages
- Urgency or pressure to act immediately
- Requests for OTPs, PINs or other sensitive information
- Suspicious external links

Users may not always recognize these signals before confirming a payment.

### The idea behind PayShield

**What if users could pause and assess the risk before they pay?**

---

## 💡 Solution

PayShield combines two complementary analysis layers:

### 1. 🔍 Transaction Risk Analysis

The system analyzes behavioral signals such as:

- Transaction amount
- Transaction time
- New beneficiary status
- Device changes
- Location changes
- Transaction frequency
- Amount deviation from usual behavior
- Beneficiary history
- Weekend activity

An **Isolation Forest** model is used to identify anomalous transaction patterns.

The ML result is combined with interpretable behavioral rules to generate:

- **Risk Score:** 0–100
- **Risk Level:** Low / Medium / High
- **Risk Factors:** Explainable reasons behind the score
- **Recommended Action**

---

### 2. 💬 Scam Message Analysis

PayShield can also analyze payment-related messages for common scam indicators.

The analyzer looks for patterns such as:

- Urgency or pressure to act quickly
- KYC/account verification requests
- Requests for sensitive credentials
- Payment or money-related language
- External links
- Unexpected rewards or prize claims
- Requests to contact external channels

The result includes:

- Scam risk score
- Risk level
- Detected indicators
- Recommended action

---

## 🧠 How It Works

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Transaction Data │        │ Payment Message │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Isolation Forest │        │ Scam Indicator   │
       │ Anomaly Detection│        │ Analysis         │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Behavioral Risk  │        │ Message Risk     │
       │ Rules            │        │ Assessment       │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                   ┌─────────────────────┐
                   │ Explainable Risk    │
                   │ Assessment          │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Risk Score          │
                   │ Risk Level          │
                   │ Risk Factors        │
                   │ Recommendation      │
                   └─────────────────────┘
