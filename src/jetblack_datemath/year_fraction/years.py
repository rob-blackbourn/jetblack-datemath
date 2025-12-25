from datetime import date
from typing import Literal

from .act_afb import act_afb

type DayCount = Literal[
    'Act/Act(AFB)'
]


def yearfrac(first: date, second: date, day_count: DayCount) -> float:

    match day_count:

        case 'Act/Act(AFB)':

            return act_afb(first, second)

        case _:

            raise ValueError("Unknown day-count convention")
