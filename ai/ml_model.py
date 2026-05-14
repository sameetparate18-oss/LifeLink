import math

# ---------------------------
# BLOOD GROUP COMPATIBILITY MAP
# ---------------------------
COMPATIBILITY = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}

# ---------------------------
# DISTANCE CALC (Haversine Formula)
# ---------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# ---------------------------
# SCORE SINGLE DONOR
# ---------------------------
def score_donor(donor, emergency):

    # 1. Check blood compatibility
    if emergency["blood_group"] not in COMPATIBILITY:
        return -1

    if donor["blood_group"] not in COMPATIBILITY[emergency["blood_group"]]:
        return -1  # not eligible

    # 2. Distance
    distance = calculate_distance(
        donor["lat"],
        donor["lon"],
        emergency["lat"],
        emergency["lon"]
    )

    # Normalize distance score (closer = better)
    distance_score = max(0, 100 - distance)

    # 3. Trust score (default 50)
    trust = donor.get("trust_score", 50)

    # 4. Urgency boost
    urgency = emergency.get("urgency", "normal")
    urgency_multiplier = 1.5 if urgency == "critical" else 1.0

    # 5. Final score
    final_score = (0.5 * distance_score + 0.5 * trust) * urgency_multiplier

    return round(final_score, 2)


# ---------------------------
# MAIN MATCHING ENGINE
# ---------------------------
def find_best_donors(donors, emergency, top_k=5):

    scored = []

    for donor in donors:
        score = score_donor(donor, emergency)

        if score != -1:
            scored.append({
                **donor,
                "score": score
            })

    # sort by score (highest first)
    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]