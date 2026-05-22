from geopy.distance import geodesic
from app.core.database import conn

blood_compatibility = {

    "O-": ["O-"],

    "O+": ["O-", "O+"],

    "A-": ["O-", "A-"],

    "A+": ["O-", "O+", "A-", "A+"],

    "B-": ["O-", "B-"],

    "B+": ["O-", "O+", "B-", "B+"],

    "AB-": ["O-", "A-", "B-", "AB-"],

    "AB+": [
        "O-",
        "O+",
        "A-",
        "A+",
        "B-",
        "B+",
        "AB-",
        "AB+"
    ]
}

def find_best_donors(

    blood_group,
    latitude,
    longitude,
    emergency

):

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    name,
    blood_group,
    city,
    latitude,
    longitude,
    available

    FROM donors

    """)

    donors = cursor.fetchall()

    matches = []

    for donor in donors:

        name = donor[0]
        blood = donor[1]
        city = donor[2]
        lat = donor[3]
        lon = donor[4]
        available = donor[5]

        if available == 0:
            continue

        compatible = blood_compatibility.get(
            blood_group,
            []
        )

        if blood not in compatible:
            continue

        distance = geodesic(

            (latitude, longitude),
            (lat, lon)

        ).km

        score = 100

        score -= distance * 0.2

        if emergency == "Critical":
            score += 50

        elif emergency == "High":
            score += 25

        matches.append({

            "name": name,
            "blood_group": blood,
            "city": city,
            "distance": round(distance, 2),
            "score": round(score, 2)

        })

    matches = sorted(

        matches,

        key=lambda x: x["score"],

        reverse=True

    )

    return matches