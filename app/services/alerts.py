def evaluate_alerts(data: dict):
    alerts = []

    heart_rate = data.get("heart_rate")
    spo2 = data.get("spo2")
    temperature = data.get("temperature")

    if heart_rate is not None:
        if heart_rate < 50 or heart_rate > 120:
            alerts.append("Abnormal heart rate")

    if spo2 is not None:
        if spo2 < 92:
            alerts.append("Low oxygen level")

    if temperature is not None:
        if temperature > 38.0:
            alerts.append("High body temperature (fever)")

    return alerts
