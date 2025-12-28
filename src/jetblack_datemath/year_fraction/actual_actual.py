from abc import ABCMeta
from calendar import isleap
from datetime import date
from typing import override

from .day_count import DayCount


class ActualActual(DayCount, metaclass=ABCMeta):
    """Base class for Act/Act"""

    @override
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        assert date1 <= date2, "Dates must the in order"

        return (date2 - date1).days


class AFB(ActualActual):

    @override
    @property
    def names(self) -> list[str]:
        return ["Act/Act AFB"]

    @override
    def years(
            self,
            date1: date,
            date2: date,
            ref_date1: date,
            ref_date2: date,
            maturity: date,
            is_eom: bool
    ) -> float:
        assert date1 <= date2, "Dates must the in order"

        if date1.year == date2.year:

            days = (date2 - date1).days
            if days == 0:
                return 0.0

            year_days = 366 if isleap(date1.year) and date1.month < 3 else 365

            return days / year_days

        else:

            days1 = (date(date1.year, 12, 31) - date1).days + 1
            year_days1 = 366 if isleap(date1.year) and date1.month < 3 else 365

            days2 = (date2 - date(date2.year, 1, 1)).days
            year_days2 = 366 if isleap(date2.year) and date2.month > 2 else 365

            year_days = date2.year - date1.year - 1

            return days1 / year_days1 + year_days + days2 / year_days2


class ISDA(ActualActual):

    @override
    @property
    def names(self) -> list[str]:
        return ["Act/Act ISDA"]

    @override
    @override
    def years(
            self,
            date1: date,
            date2: date,
            ref_date1: date,
            ref_date2: date,
            maturity: date,
            is_eom: bool
    ) -> float:
        assert date1 <= date2, "Dates must the in order"

        if date1.year == date2.year:
            days = (date2 - date1).days
            if days == 0:
                return 0.0

            year_days = 366 if isleap(date2.year) else 365
            return days / year_days

        else:
            days1 = (date(date1.year, 12, 31) - date1).days + 1
            year_days1 = 366 if isleap(date1.year) else 365

            days2 = (date2 - date(date2.year, 1, 1)).days
            year_days2 = 366 if isleap(date2.year) else 365

            year_days = date2.year - date1.year - 1
            return (days1 / year_days1) + (days2 / year_days2) + year_days


DAY_COUNTERS: list[DayCount] = [
    AFB(),
    ISDA()
]
