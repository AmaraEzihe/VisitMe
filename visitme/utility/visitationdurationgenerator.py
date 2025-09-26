from datetime import datetime, timedelta
def durationgenerator(checkindate,checkoutdate):
    ok=datetime.strptime(checkindate, "%Y-%m-%d %H:%M:%S")
    print(type(ok))
    year2 = checkoutdate.year
    month2 = checkoutdate.month
    day2= checkoutdate.day
    min2 =checkoutdate.minute
    hour2 =checkoutdate.hour
    sec2 =checkoutdate.second
    year1 = ok.year
    month1 = ok.month
    day1 = ok.day
    min1 =ok.minute
    hour1 =ok.hour
    sec1 =ok.second
    t2 = datetime(year = year2, month = month2, day = day2, hour = hour2, minute = min2, second = sec2)
    t1 = datetime(year = year1, month = month1, day = day1, hour = hour1, minute = min1, second = sec1)
    diff = t2 - t1
    return diff


def format_timedifference(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
    final = ", ".join(parts) if parts else "0 mins"
    return final
