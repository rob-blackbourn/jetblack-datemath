from datetime import date

from .day_count import DayCount
from .actual_actual import DAY_COUNTERS as DAY_COUNTERS1
from .thirty_360 import DAY_COUNTERS as DAY_COUNTERS2

DAY_COUNTERS: dict[str, DayCount] = {
    name: day_counter
    for day_counters in [
        DAY_COUNTERS1,
        DAY_COUNTERS2
    ]
    for day_counter in day_counters
    for name in day_counter.names
}


def names() -> list[str]:
    return list(DAY_COUNTERS.keys())


def days(
        date1: date,
        date2: date,
        day_count: str,
        *,
        maturity: date = date.max,
        is_eom: bool = False
) -> float:
    return DAY_COUNTERS[day_count].days(date1, date2, maturity, is_eom)


def years(
        date1: date,
        date2: date,
        day_count: str,
        *,
        ref_date1: date = date.min,
        ref_date2: date = date.max,
        maturity: date = date.max,
        is_eom: bool = False
) -> float:
    return DAY_COUNTERS[day_count].years(
        date1,
        date2,
        ref_date1,
        ref_date2,
        maturity,
        is_eom
    )


__all__ = ['names', 'days', 'years']
