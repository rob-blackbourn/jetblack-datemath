from datetime import date
from typing import Literal

from ..arithmetic import is_end_of_month

type Style = Literal[
    '30/360',
    '30A/360'
]


def _is_last_day_in_feb(value: date) -> bool:
    return (
        value.month == 2 and
        is_end_of_month(value)
    )


def d30d360e(first: date, second: date, style: Style) -> float:

    if first > second:
        return d30d360e(second, first, style)  # pylint: disable=arguments-out-of-order

    (
        y1, y2,
        m1, m2,
        d1, d2
    ) = (
        first.year, second.year,
        first.month, second.month,
        first.day, second.day
    )

    if style in ('30/360(Bond Basis)', '30A/360'):
        d1 = min(d1, 30)
        if d1 > 29:
            d2 = min(d2, 30)
    elif style in ('30/360', '30/360(US)'):

        if _is_last_day_in_feb(first) and _is_last_day_in_feb(second):
            d2 = 30
        if _is_last_day_in_feb(first):
            d1 = 30
        if d2 == 31 and (d1 == 30 or d1 == 31):
            d2 = 30
        if d1 == 31:
            d1 = 30

    if style == '30A/360':
        d1, d2 = first.day, second.day
        d1 = min(d1, 30)
        d2 = min(d2, 30)
    else:
        raise ValueError("Invalid style")

    return (
        (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360
    )
