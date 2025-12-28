from abc import ABCMeta
from datetime import date
from typing import override

from ..arithmetic import days_in_month
from .day_count import DayCount


class Thirty360(DayCount, metaclass=ABCMeta):
    """Support for 30/360 styles"""

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


def _is_last_day_in_feb(y: int, m: int, d: int) -> bool:
    return m == 2 and d == days_in_month(y, m)


def _is_last_day_of_month(y: int, m: int, d: int) -> bool:
    return d == days_in_month(y, m)


class BondBasis(Thirty360):
    """30/360 (Bond Basis)"""

    @override
    @property
    def names(self) -> list[str]:
        return ["30/360 (Bond Basis)", "30A/360"]

    @override
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        assert date1 <= date2, "Dates must the in order"

        y1, m1, d1, *_ = date1.timetuple()
        y2, m2, d2, *_ = date2.timetuple()

        d1 = min(d1, 30)
        if d1 > 29:
            d2 = min(d2, 30)

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


class US(Thirty360):
    """30/360 US"""

    @override
    @property
    def names(self) -> list[str]:
        return ["30/360 (US)"]

    @override
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        assert date1 <= date2, "Dates must the in order"

        y1, m1, d1, *_ = date1.timetuple()
        y2, m2, d2, *_ = date2.timetuple()

        if is_eom and _is_last_day_in_feb(y1, m1, d1):
            if _is_last_day_in_feb(y2, m2, d1):
                d2 = 30
            d1 = 30

        if d2 == 31 and d1 >= 30:
            d2 = 30
        if d1 == 31:
            d1 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


class Euro(Thirty360):

    @override
    @property
    def names(self) -> list[str]:
        return ["30E/360", "30/360 ICMA", "30/360 ISMA", "30S/360"]

    @override
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        assert date1 <= date2, "Dates must the in order"

        y1, m1, d1, *_ = date1.timetuple()
        y2, m2, d2, *_ = date2.timetuple()

        if d1 == 31:
            d1 = 30
        if d2 == 31:
            d2 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


class EuroISDA(Thirty360):

    @override
    @property
    def names(self) -> list[str]:
        return ["30E/360 ISDA"]

    @override
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        assert date1 <= date2, "Dates must the in order"

        y1, m1, d1, *_ = date1.timetuple()
        y2, m2, d2, *_ = date2.timetuple()

        if _is_last_day_of_month(y1, m1, d1):
            d1 = 30
        if _is_last_day_of_month(y2, m2, d2):
            if not (date2 == maturity and m2 == 2):
                d2 = 30

        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


DAY_COUNTERS: list[DayCount] = [
    US(),
    BondBasis(),
    Euro(),
    EuroISDA()
]
