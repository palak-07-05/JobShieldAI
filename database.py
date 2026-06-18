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

<<<<<<< HEAD
            ai_report TEXT
        )
        """
    )

    # Check existing columns
    c.execute(
        f"PRAGMA table_info({config.TABLE_NAME})"
    )

    columns = [col[1] for col in c.fetchall()]

    # Add ai_report column if missing
    if "ai_report" not in columns:

        c.execute(
            f"""
            ALTER TABLE {config.TABLE_NAME}
            ADD COLUMN ai_report TEXT
            """
        )
=======
        job_description TEXT,

        result TEXT

    )

    """)
>>>>>>> af6d2d2 (Added latest JobShieldAI updates)

    conn.commit()

# =========================================
# INSERT PREDICTION
# =========================================

def insert_prediction(job_description, result):

    c.execute(

        f"""
        INSERT INTO {config.TABLE_NAME} (

            job_description,
<<<<<<< HEAD
            result,
            ai_report
        )

        VALUES (?, ?, ?)
=======

            result

        )

        VALUES (?, ?)
>>>>>>> af6d2d2 (Added latest JobShieldAI updates)
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
<<<<<<< HEAD
        SELECT
            id,
            job_description,
            result,
            ai_report
        FROM {config.TABLE_NAME}
=======
        SELECT * FROM {config.TABLE_NAME}

>>>>>>> af6d2d2 (Added latest JobShieldAI updates)
        ORDER BY id DESC
        """
    )

    return c.fetchall()

# =========================================
<<<<<<< HEAD
# FETCH SINGLE RECORD
# =========================================

def fetch_by_id(record_id):

    c.execute(
        f"""
        SELECT
            id,
            job_description,
            result,
            ai_report
        FROM {config.TABLE_NAME}
        WHERE id = ?
        """,
        (record_id,)
    )

    return c.fetchone()

# =========================================
# TOTAL RECORD COUNT
# =========================================

def get_total_predictions():

    c.execute(
        f"""
        SELECT COUNT(*)
        FROM {config.TABLE_NAME}
        """
    )

    return c.fetchone()[0]

# =========================================
# FAKE JOB COUNT
# =========================================

def get_fake_count():

    c.execute(
        f"""
        SELECT COUNT(*)
        FROM {config.TABLE_NAME}
        WHERE result LIKE '%FAKE%'
        """
    )

    return c.fetchone()[0]

# =========================================
# REAL JOB COUNT
# =========================================

def get_real_count():

    c.execute(
        f"""
        SELECT COUNT(*)
        FROM {config.TABLE_NAME}
        WHERE result LIKE '%REAL%'
        """
    )

    return c.fetchone()[0]

# =========================================
=======
>>>>>>> af6d2d2 (Added latest JobShieldAI updates)
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