import sqlite3

conn = sqlite3.connect(
    "lifelink.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ================= DONORS TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS donors (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    blood_group TEXT,
    city TEXT,

    latitude REAL,
    longitude REAL,

    organ TEXT,

    available INTEGER,

    reward_points INTEGER DEFAULT 0

)

""")

# ================= ALERTS TABLE =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS alerts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    message TEXT,
    city TEXT

)

""")

conn.commit()