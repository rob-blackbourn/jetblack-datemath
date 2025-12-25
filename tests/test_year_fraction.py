from datetime import date
from jetblack_datemath import yearfrac, DayCount


def test_act_afb() -> None:
    params: list[tuple[date, date, DayCount, float, int]] = [

        (date(2000, 1, 1), date(2001, 1, 1), 'Act/Act(AFB)', 1.0, 8),
        (date(2018, 12, 15), date(2019, 3, 1), 'Act/Act(AFB)', 0.20821918, 8),
        (date(2018, 12, 31), date(2019, 1, 1), 'Act/Act(AFB)', 1 / 365, 8),
        (date(1994, 6, 30), date(1997, 6, 30), 'Act/Act(AFB)', 3.0, 8),
        (date(1994, 2, 10), date(1994, 6, 30), 'Act/Act(AFB)', 140 / 365, 8),

        (date(2000, 1, 1), date(2001, 1, 1), 'Act/Act(ISDA)', 1.0, 8),
        (date(2018, 12, 15), date(2019, 3, 1), 'Act/Act(ISDA)', 0.20821918, 8),
        (date(2018, 12, 31), date(2019, 1, 1), 'Act/Act(ISDA)', 1 / 365, 8),
        (date(1994, 6, 30), date(1997, 6, 30), 'Act/Act(ISDA)', 3.0, 8),
        (date(1994, 2, 10), date(1994, 6, 30), 'Act/Act(ISDA)', 140 / 365, 8)
    ]
    for first, second, day_count, expected, ndigits in params:
        actual = yearfrac(first, second, day_count)
        assert round(actual, ndigits) == round(expected, ndigits)
