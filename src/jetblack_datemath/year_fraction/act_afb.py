"""Months"""

from calendar import isleap
from datetime import date


def act_afb(first: date, second: date) -> float:

    if first > second:

        return act_afb(second, first)  # pylint: disable=arguments-out-of-order

    elif first.year == second.year:

        diff_days = (second - first).days
        if diff_days == 0:
            return 0.0

        denom = 366 if isleap(first.year) and first.month < 3 else 365

        return diff_days / denom

    else:

        diff1 = (date(first.year, 12, 31) - first).days + 1
        denom1 = 366 if isleap(first.year) and first.month < 3 else 365

        diff2 = (second - date(second.year, 1, 1)).days
        denom2 = 366 if isleap(second.year) and second.month >= 3 else 365

        diff_years = second.year - first.year - 1
        return diff1 / denom1 + diff2 / denom2 + diff_years
