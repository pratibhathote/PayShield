import os
import numpy as np
import pandas as pd

# Reproducible results
np.random.seed(42)

# Number of synthetic transactions
N = 5000

data = {
    "amount": np.round(np.random.lognormal(mean=7.0, sigma=1.0, size=N), 2),
    "hour": np.random.randint(0, 24, N),
    "new_beneficiary": np.random.choice([0, 1], N, p=[0.85, 0.15]),
    "device_changed": np.random.choice([0, 1], N, p=[0.90, 0.10]),
    "location_changed": np.random.choice([0, 1], N, p=[0.92, 0.08]),
    "transactions_today": np.random.randint(1, 15, N),
    "amount_deviation": np.round(
        np.random.lognormal(mean=0.5, sigma=1.0, size=N), 2
    ),
    "beneficiary_age_days": np.random.randint(0, 1500, N),
    "is_weekend": np.random.choice([0, 1], N, p=[0.71, 0.29]),
}

df = pd.DataFrame(data)

# Make beneficiary age 0 for new beneficiaries
df.loc[df["new_beneficiary"] == 1, "beneficiary_age_days"] = 0

# Add a small amount of realistic correlation:
# New beneficiaries are more likely to have device/location changes.
new_beneficiary_mask = df["new_beneficiary"] == 1

df.loc[new_beneficiary_mask, "device_changed"] = np.random.choice(
    [0, 1],
    size=new_beneficiary_mask.sum(),
    p=[0.55, 0.45],
)

df.loc[new_beneficiary_mask, "location_changed"] = np.random.choice(
    [0, 1],
    size=new_beneficiary_mask.sum(),
    p=[0.65, 0.35],
)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save dataset
output_path = "data/transactions.csv"
df.to_csv(output_path, index=False)

print(f"Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset statistics:")
print(df.describe())