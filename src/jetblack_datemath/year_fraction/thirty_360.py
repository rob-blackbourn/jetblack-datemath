from abc import ABCMeta
from datetime import date
from typing import override

from ..arithmetic import is_end_of_month
from .day_count import DayCount


class ThirtyThreeSixty(DayCount, metaclass=ABCMeta):
    """Support for 30/360 styles"""

    @override
    def years(self, start: date, end: date, ref_start: date, ref_end: date) -> float:
        return self.days(start, end) / 360


def _is_last_day_in_feb(value: date) -> bool:
    return (
        value.month == 2 and
        is_end_of_month(value)
    )


class US(ThirtyThreeSixty):
    """Support for 30/360 US"""

    @override
    @property
    def names(self) -> list[str]:
        return ["30/360 (US)"]

    @override
    def days(self, start: date, end: date) -> int:
        y1, m1, d1, *_ = start.timetuple()
        y2, m2, d2, *_ = end.timetuple()

        if _is_last_day_in_feb(start):
            if _is_last_day_in_feb(end):
                d2 = 30
            d1 = 30

        if d2 == 31 and d1 >= 30:
            d2 = 30
        if d1 == 31:
            d1 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


class BondBasis(ThirtyThreeSixty):

    @override
    @property
    def names(self) -> list[str]:
        return ["30/360 (Bond Basis)", "30A/360"]

    @override
    def days(self, start: date, end: date) -> int:
        y1, m1, d1, *_ = start.timetuple()
        y2, m2, d2, *_ = end.timetuple()

        d1 = min(d1, 30)
        if d1 > 29:
            d2 = min(d2, 30)

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


class ISMA(ThirtyThreeSixty):

    @override
    @property
    def names(self) -> list[str]:
        return ["30/360 (ISMA)"]

    @override
    def days(self, start: date, end: date) -> int:
        y1, m1, d1, *_ = start.timetuple()
        y2, m2, d2, *_ = end.timetuple()

        if d1 == 31:
            d1 = 30
        if d2 == 31 and d1 == 30:
            d2 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


def d30d360e(first: date, second: date, feb_30d: bool) -> int:

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

    return days


class Euro(ThirtyThreeSixty):

    @override
    @property
    def names(self) -> list[str]:
        return ["30E/360"]

    @override
    def days(self, start: date, end: date) -> int:
        return d30d360e(start, end, True)


DAY_COUNTERS: list[DayCount] = [
    US(),
    BondBasis(),
    ISMA()
]
