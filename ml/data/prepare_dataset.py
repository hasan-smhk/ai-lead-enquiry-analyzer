"""
ml/data/prepare_dataset.py
Converts the raw JZD dataset into the standardized schema needed for training.

Run from project root:
    python ml/data/prepare_dataset.py
"""

import os
import pandas as pd

INPUT_PATH = os.path.join("ml", "data", "raw", "original_dataset.csv")
OUTPUT_PATH = os.path.join("ml", "data", "raw", "enquiries.csv")

VALID_URGENCY = {"Low", "Medium", "High"}
HIGH_BUDGET_THRESHOLD = 500_000
MEDIUM_BUDGET_THRESHOLD = 100_000
PRIORITY_RANK = {"Low": 0, "Medium": 1, "High": 2}


def budget_to_priority(budget) -> str:
    if pd.isna(budget):
        return "Low"
    budget = float(budget)
    if budget >= HIGH_BUDGET_THRESHOLD:
        return "High"
    if budget >= MEDIUM_BUDGET_THRESHOLD:
        return "Medium"
    return "Low"


def derive_priority(row) -> str:
    urgency = row["urgency_hint"] if row["urgency_hint"] in VALID_URGENCY else "Low"
    budget_priority = budget_to_priority(row.get("budget_inr"))
    return urgency if PRIORITY_RANK[urgency] >= PRIORITY_RANK[budget_priority] else budget_priority


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Could not find {INPUT_PATH}. Did you copy your CSV there?")

    df = pd.read_csv(INPUT_PATH)
    print("Columns found in your file:", df.columns.tolist())

    required = ["enquiry_id", "enquiry_text", "industry", "primary_service", "budget_inr", "urgency_hint"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    df = df.rename(columns={"enquiry_text": "text", "primary_service": "category"})

    df = df.dropna(subset=["text", "category"])
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 0]

    invalid_urgency = ~df["urgency_hint"].isin(VALID_URGENCY)
    if invalid_urgency.any():
        print(f"WARNING: {invalid_urgency.sum()} rows have unexpected urgency_hint; defaulting to 'Low'.")
        df.loc[invalid_urgency, "urgency_hint"] = "Low"

    df["priority"] = df.apply(derive_priority, axis=1)

    final_cols = ["enquiry_id", "text", "category", "industry", "budget_inr", "urgency_hint", "priority"]
    df = df[final_cols]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSUCCESS: Prepared {len(df)} rows -> {OUTPUT_PATH}")
    print("\nCategory distribution:\n", df["category"].value_counts())
    print("\nPriority distribution:\n", df["priority"].value_counts())


if __name__ == "__main__":
    main()
