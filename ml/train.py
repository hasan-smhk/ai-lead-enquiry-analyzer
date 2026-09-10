"""
ml/train.py
Trains category_classifier and priority_classifier models.

Run from inside the ml/ folder:
    cd ml
    python train.py
"""

import os
import json
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

from preprocess import clean_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

RAW_DATA_PATH = os.path.join("data", "raw", "enquiries.csv")
PROCESSED_DIR = os.path.join("data", "processed")
MODEL_DIR = os.getenv("MODEL_DIR", "models")
REPORTS_DIR = "reports"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data() -> pd.DataFrame:
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"{RAW_DATA_PATH} not found. Run ml/data/prepare_dataset.py first.")
    df = pd.read_csv(RAW_DATA_PATH)
    df = df.dropna(subset=["text", "category", "priority"])
    df["text"] = df["text"].apply(clean_text)
    df = df[df["text"].str.len() > 0]
    logger.info("Loaded %d valid rows", len(df))
    return df


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000, stop_words="english", sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE)),
    ])


def train_and_evaluate(df: pd.DataFrame, target_col: str, model_name: str):
    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=df[target_col]
    )

    pipeline = build_pipeline()
    pipeline.fit(train_df["text"], train_df[target_col])

    preds = pipeline.predict(test_df["text"])
    acc = accuracy_score(test_df[target_col], preds)
    report = classification_report(test_df[target_col], preds, output_dict=True)
    cm = confusion_matrix(test_df[target_col], preds).tolist()
    labels = sorted(test_df[target_col].unique().tolist())

    logger.info("[%s] Test Accuracy: %.4f", model_name, acc)

    joblib.dump(pipeline, os.path.join(MODEL_DIR, f"{model_name}.joblib"))
    test_df[["text", target_col]].to_csv(os.path.join(PROCESSED_DIR, f"test_{model_name}.csv"), index=False)

    metrics = {
        "model": model_name, "target": target_col, "accuracy": acc,
        "classification_report": report, "confusion_matrix": cm, "labels": labels,
        "train_size": len(train_df), "test_size": len(test_df),
    }
    with open(os.path.join(REPORTS_DIR, f"metrics_{model_name}.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    with open(os.path.join(REPORTS_DIR, f"metrics_{model_name}.md"), "w") as f:
        f.write(f"# {model_name} Evaluation Report\n\n**Accuracy:** {acc:.4f}\n\n")
        f.write("| Label | Precision | Recall | F1-score | Support |\n|---|---|---|---|---|\n")
        for label in labels:
            r = report[label]
            f.write(f"| {label} | {r['precision']:.2f} | {r['recall']:.2f} | {r['f1-score']:.2f} | {int(r['support'])} |\n")

    return metrics


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    df = load_data()

    logger.info("Training category classifier...")
    train_and_evaluate(df, "category", "category_classifier")

    logger.info("Training priority classifier...")
    train_and_evaluate(df, "priority", "priority_classifier")


if __name__ == "__main__":
    main()
