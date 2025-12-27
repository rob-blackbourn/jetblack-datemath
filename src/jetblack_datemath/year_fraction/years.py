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


def years(
        day_count: str,
        first: date,
        second: date,
        ref_start: date = date.min,
        ref_end: date = date.max
) -> float:
    return DAY_COUNTERS[day_count].years(first, second, ref_start, ref_end)
