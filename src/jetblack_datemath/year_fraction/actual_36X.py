from abc import ABCMeta
from datetime import date
from typing import override

from .day_count import DayCount


class Actual36X(DayCount, metaclass=ABCMeta):
    """Act/365"""

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


class Actual360(Actual36X):
    """Act/365"""

    @override
    @property
    def names(self) -> list[str]:
        return ["Act/365 Fixed"]

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

        return self.days(date1, date2, maturity, is_eom) / 360


class Actual365(Actual36X):
    """Act/365"""

    @override
    @property
    def names(self) -> list[str]:
        return ["Act/365", "Act/365 Fixed"]

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

        return self.days(date1, date2, maturity, is_eom) / 365


DAY_COUNTERS: list[DayCount] = [
    Actual360(),
    Actual365()
]
