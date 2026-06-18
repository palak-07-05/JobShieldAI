from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================
# MODEL CONFIGURATION
# =========================================

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# =========================================
# TRAINING SETTINGS
# =========================================

RANDOM_STATE = 42

TEST_SIZE = 0.2

# =========================================
# APPLICATION SETTINGS
# =========================================

APP_TITLE = "JobShield AI"

APP_ICON = "🛡️"

APP_LAYOUT = "wide"

# =========================================
# DATABASE SETTINGS
# =========================================

DATABASE_NAME = os.path.join(BASE_DIR, "jobshield.db")

TABLE_NAME = "predictions"

# =========================================
# MODEL SETTINGS
# =========================================

MAX_FEATURES = 10000

NGRAM_RANGE = (1, 2)

MIN_DF = 2

STOP_WORDS = "english"

# =========================================
# UI COLORS
# =========================================

PRIMARY_COLOR = "#9333ea"

SECONDARY_COLOR = "#c084fc"

BACKGROUND_COLOR = "#050816"

CARD_COLOR = "rgba(15, 23, 42, 0.72)"

TEXT_COLOR = "#E2E8F0"

# =========================================
# FRAUD THRESHOLDS
# =========================================

LOW_RISK = 30

MEDIUM_RISK = 70

# =========================================
# DASHBOARD SETTINGS
# =========================================

CHART_HEIGHT = 400

PIE_CHART_SIZE = (5, 5)

# =========================================
# DEFAULT TEXT
# =========================================

PLACEHOLDER_TEXT = """
Paste complete job description here...

Example:
Company hiring urgently for remote work.
No experience required.
Weekly payout available.
Apply now.
"""

EMPTY_INPUT_MESSAGE = "Please enter a job description."

NO_HISTORY_MESSAGE = "No prediction history found."

NO_DATA_MESSAGE = "No prediction data available yet."

# =========================================
# GEMINI API SETTINGS
# =========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"
