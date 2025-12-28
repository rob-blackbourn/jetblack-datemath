from datetime import date

from .day_count import DayCount
from .actual_actual import DAY_COUNTERS as _DAY_COUNTERS1
from .thirty_360 import DAY_COUNTERS as _DAY_COUNTERS2

_DAY_COUNTERS: dict[str, DayCount] = {
    name: day_counter
    for day_counters in [
        _DAY_COUNTERS1,
        _DAY_COUNTERS2
    ]
    for day_counter in day_counters
    for name in day_counter.names
}


def names() -> list[str]:
    return list(_DAY_COUNTERS.keys())


def day_counter(name: str) -> DayCount:
    return _DAY_COUNTERS[name]


def days(
        date1: date,
        date2: date,
        day_count: str,
        *,
        maturity: date = date.max,
        is_eom: bool = False
) -> float:
    return day_counter(day_count).days(date1, date2, maturity, is_eom)


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
    return day_counter(day_count).years(
        date1,
        date2,
        ref_date1,
        ref_date2,
        maturity,
        is_eom
    )


__all__ = ['names', 'day_counter', 'days', 'years', 'DayCount']
