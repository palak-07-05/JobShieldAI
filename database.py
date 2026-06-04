import sqlite3
import config

# =========================================
# CONNECT DATABASE
# =========================================

conn = sqlite3.connect(

    config.DATABASE_NAME,

    check_same_thread=False
)

c = conn.cursor()

# =========================================
# INITIALIZE DATABASE
# =========================================

def init_db():

    c.execute(f"""

    CREATE TABLE IF NOT EXISTS {config.TABLE_NAME} (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        job_description TEXT,

        result TEXT

    )

    """)

    conn.commit()

# =========================================
# INSERT PREDICTION
# =========================================

def insert_prediction(job_description, result):

    c.execute(

        f"""
        INSERT INTO {config.TABLE_NAME} (

            job_description,

            result

        )

        VALUES (?, ?)
        """,

        (

            job_description,

            result
        )
    )

    conn.commit()

# =========================================
# FETCH ALL RECORDS
# =========================================

def fetch_all():

    c.execute(

        f"""
        SELECT * FROM {config.TABLE_NAME}

        ORDER BY id DESC
        """
    )

    return c.fetchall()

# =========================================
# CLEAR HISTORY
# =========================================

def clear_history():

    c.execute(

        f"DELETE FROM {config.TABLE_NAME}"
    )

    conn.commit()

# =========================================
# CLOSE CONNECTION
# =========================================

def close_connection():

    conn.close()