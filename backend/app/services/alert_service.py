alerts = []

def create_alert(message, city):

    data = {

        "message": message,
        "city": city

    }

    alerts.append(data)

    return data


def get_alerts():

    return alerts