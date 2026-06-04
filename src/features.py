import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================
# TF-IDF VECTORIZER
# =========================================

def get_vectorizer():

    return TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=2
    )

# =========================================
# FEATURE ENGINEERING
# =========================================

def add_features(df):

    # =========================================
    # REQUIRED COLUMNS
    # =========================================

    required_columns = [

        "title",
        "company_profile",
        "description",
        "requirements",
        "benefits"
    ]

    # ADD MISSING COLUMNS SAFELY

    for col in required_columns:

        if col not in df.columns:

            df[col] = ""

    # =========================================
    # CREATE MAIN TEXT COLUMN
    # =========================================

    df["text"] = (

        df["title"].fillna("").astype(str) + " " +

        df["company_profile"].fillna("").astype(str) + " " +

        df["description"].fillna("").astype(str) + " " +

        df["requirements"].fillna("").astype(str) + " " +

        df["benefits"].fillna("").astype(str)
    )

    # =========================================
    # CLEAN TEXT
    # =========================================

    df["text"] = (

        df["text"]

        .str.lower()

        .str.replace(r"\s+", " ", regex=True)

        .str.strip()
    )

    # =========================================
    # SCAM FEATURES
    # =========================================

    # PAYMENT / FEES

    df["has_fee"] = df["text"].str.contains(

        r"fee|payment|registration|deposit|processing fee|security amount",

        regex=True,
        na=False

    ).astype(int)

    # URGENCY WORDS

    df["has_urgent"] = df["text"].str.contains(

        r"urgent|apply now|limited seats|immediate joining|quick hiring",

        regex=True,
        na=False

    ).astype(int)

    # MONEY ATTRACTION

    df["has_money_words"] = df["text"].str.contains(

        r"high salary|easy money|earn money|weekly payout|daily payout",

        regex=True,
        na=False

    ).astype(int)

    # REMOTE JOB SCAMS

    df["has_remote_words"] = df["text"].str.contains(

        r"work from home|remote job|online work|part time online",

        regex=True,
        na=False

    ).astype(int)

    # CONTACT METHODS

    df["has_contact"] = df["text"].str.contains(

        r"whatsapp|telegram|dm now|call now|contact us",

        regex=True,
        na=False

    ).astype(int)

    # NO EXPERIENCE CLAIMS

    df["has_no_experience"] = df["text"].str.contains(

        r"no experience|freshers welcome|anyone can apply",

        regex=True,
        na=False

    ).astype(int)

    # UNREALISTIC PROMISES

    df["has_unrealistic_offer"] = df["text"].str.contains(

        r"guaranteed job|instant joining|earn instantly|easy work",

        regex=True,
        na=False

    ).astype(int)

    # =========================================
    # TEXT FEATURES
    # =========================================

    # EXCLAMATION MARKS

    df["exclamation_count"] = (

        df["text"]
        .str.count(r"!")
    )

    # CAPITAL WORD COUNT

    df["capital_word_count"] = df["text"].apply(

        lambda x: sum(

            1 for word in str(x).split()

            if word.isupper()
        )
    )

    # TEXT LENGTH

    df["text_length"] = df["text"].apply(len)

    # WORD COUNT

    df["word_count"] = df["text"].apply(

        lambda x: len(str(x).split())
    )

    # AVERAGE WORD LENGTH

    df["avg_word_length"] = df["text"].apply(

        lambda x: (

            sum(len(word) for word in str(x).split())

            / len(str(x).split())

        ) if len(str(x).split()) > 0 else 0
    )

    # =========================================
    # FINAL CLEANUP
    # =========================================

    df = df.fillna(0)

    return df