from app.core.database import conn

def donor_analytics():

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM donors"
    )

    total = cursor.fetchone()[0]

    cursor.execute("""

    SELECT blood_group, COUNT(*)

    FROM donors

    GROUP BY blood_group

    """)

    blood_data = cursor.fetchall()

    return {

        "total_donors": total,
        "blood_stats": blood_data

    }