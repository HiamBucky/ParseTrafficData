from datetime import datetime


def store_status(time: str, day: str):
    nine_am = datetime.strptime("09:00", "%H:%M").time()
    seven_thirty_am = datetime.strptime("07:30", "%H:%M").time()
    six_pm = datetime.strptime("18:00", "%H:%M").time()
    seven_pm = datetime.strptime("19:00", "%H:%M").time()
    nine_pm = datetime.strptime("21:00", "%H:%M").time()
    ten_pm = datetime.strptime("22:00", "%H:%M").time()
    time_of_day = datetime.strptime(time, "%H:%M").time()
    if day == "SUNDAY":
        return "CLOSED"
    if time_of_day >= seven_thirty_am and time_of_day < nine_am:
        return "OPENING"
    if day in ["MONDAY", "WEDNESDAY", "SATURDAY"]:
        if time_of_day >= nine_am and time_of_day < six_pm:
            return "OPEN"
        if time_of_day >= six_pm and time_of_day <= seven_pm:
            return "CLOSING"
    if day in ["TUESDAY", "THURSDAY", "FRIDAY"]:
        if time_of_day >= nine_am and time_of_day < nine_pm:
            return "OPEN"
        if time_of_day >= nine_pm and time_of_day <= ten_pm:
            return "CLOSING"
    return "CLOSED"
