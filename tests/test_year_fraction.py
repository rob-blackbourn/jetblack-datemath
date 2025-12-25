from datetime import date
from jetblack_datemath import yearfrac, DayCount


def test_act_afb() -> None:
    params: list[tuple[date, date, DayCount, float]] = [
        (date(2000, 1, 1), date(2001, 1, 1), 'Act/Act(AFB)', 1.0)
    ]
    for first, second, day_count, expected in params:
        actual = yearfrac(first, second, day_count)
        assert actual, expected
