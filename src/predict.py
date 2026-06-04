import pickle
import os

from src.preprocess import clean_text
import config

# =========================================
# LOAD MODEL & VECTORIZER
# =========================================

# CHECK MODEL FILE

if not os.path.exists(config.MODEL_PATH):

    raise FileNotFoundError(
        f"Model file not found: {config.MODEL_PATH}"
    )

# CHECK VECTORIZER FILE

if not os.path.exists(config.VECTORIZER_PATH):

    raise FileNotFoundError(
        f"Vectorizer file not found: {config.VECTORIZER_PATH}"
    )

# LOAD TRAINED MODEL

with open(config.MODEL_PATH, "rb") as model_file:

    model = pickle.load(model_file)

# LOAD TF-IDF VECTORIZER

with open(config.VECTORIZER_PATH, "rb") as vectorizer_file:

    vectorizer = pickle.load(vectorizer_file)

# =========================================
# PREDICTION FUNCTION
# =========================================

def predict_job(text):

    # =========================================
    # HANDLE EMPTY INPUT
    # =========================================

    if not text or len(text.strip()) == 0:

        return {

            "prediction": -1,

            "fake_score": 0,

            "real_score": 0,

            "message": "Empty job description"
        }

    try:

        # =========================================
        # CLEAN INPUT TEXT
        # =========================================

        cleaned_text = clean_text(text)

        # =========================================
        # VECTORIZE TEXT
        # =========================================

        vector = vectorizer.transform(
            [cleaned_text]
        )

        # =========================================
        # MODEL PREDICTION
        # =========================================

        prediction = model.predict(vector)[0]

        # =========================================
        # PROBABILITY SCORES
        # =========================================

        fake_score = 0
        real_score = 0

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(vector)[0]

            # ASSUMING:
            # 0 = REAL
            # 1 = FAKE

            real_score = round(
                probabilities[0] * 100,
                2
            )

            fake_score = round(
                probabilities[1] * 100,
                2
            )

        # =========================================
        # RETURN RESULT
        # =========================================

        return {

            "prediction": int(prediction),

            "fake_score": fake_score,

            "real_score": real_score,

            "message": "Prediction successful"
        }

    except Exception as e:

        return {

            "prediction": -1,

            "fake_score": 0,

            "real_score": 0,

            "message": f"Prediction error: {str(e)}"
        }