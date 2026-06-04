import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from src.preprocess import clean_text
from src.features import get_vectorizer

import config

# =========================================
# CHECK DATASET
# =========================================

DATASET_PATH = "fake_job_postings.csv"

if not os.path.exists(DATASET_PATH):

    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

# =========================================
# LOAD DATASET
# =========================================

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Dataset Loaded: {df.shape}")

# =========================================
# REQUIRED COLUMNS CHECK
# =========================================

required_columns = [
    "description",
    "fraudulent"
]

for col in required_columns:

    if col not in df.columns:

        raise ValueError(
            f"Missing required column: {col}"
        )

# =========================================
# KEEP REQUIRED COLUMNS
# =========================================

df = df[
    [
        "description",
        "fraudulent"
    ]
]

# =========================================
# REMOVE NULL VALUES
# =========================================

df.dropna(inplace=True)

print(f"After removing nulls: {df.shape}")

# =========================================
# CLEAN TEXT
# =========================================

print("\nCleaning text data...")

df["cleaned"] = df["description"].apply(
    clean_text
)

# Remove empty cleaned text

df = df[
    df["cleaned"].str.strip() != ""
]

# =========================================
# FEATURES & LABELS
# =========================================

X = df["cleaned"]

y = df["fraudulent"]

# =========================================
# TRAIN TEST SPLIT
# =========================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=config.TEST_SIZE,

    random_state=config.RANDOM_STATE,

    stratify=y
)

# =========================================
# TF-IDF VECTORIZER
# =========================================

print("\nCreating TF-IDF vectors...")

vectorizer = get_vectorizer()

X_train_vec = vectorizer.fit_transform(
    X_train
)

X_test_vec = vectorizer.transform(
    X_test
)

# =========================================
# MACHINE LEARNING MODEL
# =========================================

print("\nTraining Logistic Regression Model...")

model = LogisticRegression(

    max_iter=1000,

    random_state=config.RANDOM_STATE
)

model.fit(
    X_train_vec,
    y_train
)

# =========================================
# MODEL EVALUATION
# =========================================

print("\nEvaluating model...")

predictions = model.predict(
    X_test_vec
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n===================================")
print("MODEL TRAINING COMPLETED")
print("===================================\n")

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# =========================================
# SAVE MODEL
# =========================================

print("\nSaving model files...")

with open(config.MODEL_PATH, "wb") as model_file:

    pickle.dump(
        model,
        model_file
    )

with open(config.VECTORIZER_PATH, "wb") as vectorizer_file:

    pickle.dump(
        vectorizer,
        vectorizer_file
    )

# =========================================
# SUCCESS MESSAGE
# =========================================

print("\n===================================")
print("FILES SAVED SUCCESSFULLY")
print("===================================\n")

print(f"Model Path: {config.MODEL_PATH}")
print(f"Vectorizer Path: {config.VECTORIZER_PATH}")

print("\n✅ Training Completed Successfully")