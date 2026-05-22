def calculate_reward(donations):

    if donations >= 20:
        return 1000

    elif donations >= 10:
        return 500

    elif donations >= 5:
        return 200

    else:
        return 50
    