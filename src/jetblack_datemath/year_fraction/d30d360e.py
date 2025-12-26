from datetime import date


def d30d360e(first: date, second: date, feb_30d: bool) -> float:

    if first > second:
        return d30d360e(second, first, feb_30d)  # pylint: disable=arguments-out-of-order

    days = 0
    days += 360 * (second.year - first.year)
    days += 30 * (second.month - first.month)
    if not (second.month == 2 and second.day >= 28):
        days += 30 if second.day > 30 else second.day
    elif feb_30d:
        days += 30
    else:
        days += second.day

    if (first.month == 2) and (first.day >= 28):
        days -= 30
    else:
        days -= 30 if first.day > 30 else first.day

    if days == 0:
        return 0.0
    else:
        return days / 360
