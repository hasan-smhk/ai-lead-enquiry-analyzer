"""
ml/evaluate.py
Re-checks saved models against their held-out test sets.

Run from inside ml/ folder:
    python evaluate.py
"""

import os
import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score

MODEL_DIR = "models"
PROCESSED_DIR = os.path.join("data", "processed")

MODELS = ["category_classifier", "priority_classifier"]


def main():
    for name in MODELS:
        model_path = os.path.join(MODEL_DIR, f"{name}.joblib")
        test_path = os.path.join(PROCESSED_DIR, f"test_{name}.csv")

        if not os.path.exists(model_path) or not os.path.exists(test_path):
            print(f"Skipping {name}: run train.py first.")
            continue

        pipeline = joblib.load(model_path)
        test_df = pd.read_csv(test_path)
        target_col = "category" if "category" in test_df.columns else "priority"

        preds = pipeline.predict(test_df["text"])
        acc = accuracy_score(test_df[target_col], preds)

        print(f"\n===== {name} =====")
        print(f"Accuracy: {acc:.4f}")
        print(classification_report(test_df[target_col], preds))


if __name__ == "__main__":
    main()
