from calendar import isleap
from datetime import date
from typing import override

from .day_count import DayCount


class ActualActual(DayCount):

    @override
    def days(self, start: date, end: date) -> int:
        return (end - start).days


class AFB(ActualActual):

    @override
    @property
    def names(self) -> list[str]:
        return ["Actual/Actual (AFB)"]

    @override
    def years(self, start: date, end: date, ref_start: date, ref_end: date) -> float:

        if start > end:

            return self.years(end, start, ref_start, ref_end)  # pylint: disable=arguments-out-of-order

        elif start.year == end.year:

            diff_days = (end - start).days
            if diff_days == 0:
                return 0.0

            denom = 366 if isleap(start.year) and start.month < 3 else 365

            return diff_days / denom

        else:

            diff1 = (date(start.year, 12, 31) - start).days + 1
            denom1 = 366 if isleap(start.year) and start.month < 3 else 365

            diff2 = (end - date(end.year, 1, 1)).days
            denom2 = 366 if isleap(end.year) and end.month >= 3 else 365

            diff_years = end.year - start.year - 1
            return diff1 / denom1 + diff2 / denom2 + diff_years


class ISDA(ActualActual):

    @override
    @property
    def names(self) -> list[str]:
        return ["Actual/Actual (ISDA)"]

    @override
    def years(self, start: date, end: date, ref_start: date, ref_end: date) -> float:
        if start > end:

            return self.years(end, start, ref_start, ref_end)  # pylint: disable=arguments-out-of-order

        if start.year == end.year:
            diff_days = (end - start).days
            if diff_days == 0:
                return 0.0

            denom = 366 if isleap(end.year) else 365
            return diff_days / denom

        else:
            diff1 = (date(start.year, 12, 31) - start).days + 1
            denom1 = 366 if isleap(start.year) else 365

            diff2 = (end - date(end.year, 1, 1)).days
            denom2 = 366 if isleap(end.year) else 365

            diff_years = end.year - start.year - 1
            return (diff1 / denom1) + (diff2 / denom2) + diff_years


DAY_COUNTERS: list[DayCount] = [
    AFB(),
    ISDA()
]
