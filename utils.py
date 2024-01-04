# utils.py
import datetime
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "morning"
    elif hour >= 12 and hour < 18:
        return "afternoon"
    else:
        return "evening"