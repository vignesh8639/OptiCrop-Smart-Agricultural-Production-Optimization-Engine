import sqlite3

DATABASE = "database.db"


def get_connection():
    """
    Create and return a database connection.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """
    Create all required tables if they do not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # Users Table
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
    # ==========================
    # Prediction History Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,

            nitrogen REAL NOT NULL,
            phosphorus REAL NOT NULL,
            potassium REAL NOT NULL,

            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            ph REAL NOT NULL,
            rainfall REAL NOT NULL,

            predicted_crop TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(fullname, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (fullname, email, password)
        VALUES (?, ?, ?)
    """, (fullname, email, password))

    conn.commit()
    conn.close()


def get_user(username):
    """
    Get user by username.
    """

    conn = get_connection()

    user = conn.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,)).fetchone()

    conn.close()

    return user


def save_prediction(
    user_id,
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
    predicted_crop
):
    """
    Save prediction history.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history
        (
            user_id,
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
            predicted_crop
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        nitrogen,
        phosphorus,
        potassium,
        temperature,
        humidity,
        ph,
        rainfall,
        predicted_crop
    ))

    conn.commit()
    conn.close()


def get_prediction_history(user_id):
    """
    Return prediction history for a user.
    """

    conn = get_connection()

    history = conn.execute("""
        SELECT *
        FROM prediction_history
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    conn.close()

    return history


if __name__ == "__main__":
    create_tables()
    print("=" * 50)
    print(" Smart Agriculture Database Created Successfully ")
    print("=" * 50)
    