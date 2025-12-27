from datetime import date
from jetblack_datemath.year_fraction import years, days


def test_thirty_360_bond_basis() -> None:
    """Test for 30/360 (Bond Basis)"""

    # See https://www.isda.org/2008/12/22/30-360-day-count-conventions/

    data: list[tuple[date, date, int]] = [
        # Example 1: End dates do not involve the last day of February
        (date(2006, 8, 20), date(2007, 2, 20), 180),
        (date(2007, 2, 20), date(2007, 8, 20), 180),
        (date(2007, 8, 20), date(2008, 2, 20), 180),
        (date(2008, 2, 20), date(2008, 8, 20), 180),
        (date(2008, 8, 20), date(2009, 2, 20), 180),
        (date(2009, 2, 20), date(2009, 8, 20), 180),

        # Example 2: End dates include some end-2 dates
        (date(2006, 8, 31), date(2007, 2, 28), 178),
        (date(2007, 2, 28), date(2007, 8, 31), 183),
        (date(2007, 8, 31), date(2008, 2, 29), 179),
        (date(2008, 2, 29), date(2008, 8, 31), 182),
        (date(2008, 8, 31), date(2009, 2, 28), 178),
        (date(2009, 2, 28), date(2009, 8, 31), 183),

        # Example 3: Miscellaneous calculations
        (date(2006, 1, 31), date(2006, 2, 28), 28),
        (date(2006, 1, 30), date(2006, 2, 28), 28),
        (date(2006, 2, 28), date(2006, 3, 3), 5),
        (date(2006, 2, 14), date(2006, 2, 28), 14),
        (date(2006, 9, 30), date(2006, 10, 31), 30),
        (date(2006, 10, 31), date(2006, 11, 28), 28),
        (date(2007, 8, 31), date(2008, 2, 28), 178),
        (date(2008, 2, 28), date(2008, 8, 28), 180),
        (date(2008, 2, 28), date(2008, 8, 30), 182),
        (date(2008, 2, 28), date(2008, 8, 31), 183),
        (date(2007, 2, 26), date(2008, 2, 28), 362),
        (date(2007, 2, 26), date(2008, 2, 29), 363),
        (date(2008, 2, 29), date(2009, 2, 28), 359),
        (date(2008, 2, 28), date(2008, 3, 30), 32),
        (date(2008, 2, 28), date(2008, 3, 31), 33)
    ]

    for start, end, expected in data:
        actual = days("30/360 (Bond Basis)", start, end)
        assert expected == actual, f"{start} to {end}: {actual} != {expected}"


def test_act_act() -> None:
    params: list[tuple[date, date, str, float, int]] = [

        (date(2000, 1, 1), date(2001, 1, 1), 'Actual/Actual (AFB)', 1.0, 8),
        # (date(2018, 12, 15), date(2019, 3, 1), 'Actual/Actual (AFB)', 0.20821918, 8),
        # (date(2018, 12, 31), date(2019, 1, 1), 'Actual/Actual (AFB)', 1 / 365, 8),
        # (date(1994, 6, 30), date(1997, 6, 30), 'Actual/Actual (AFB)', 3.0, 8),
        # (date(1994, 2, 10), date(1994, 6, 30), 'Actual/Actual (AFB)', 140 / 365, 8),

        # (date(2000, 1, 1), date(2001, 1, 1), 'Actual/Actual (ISDA)', 1.0, 8),
        # (date(2018, 12, 15), date(2019, 3, 1), 'Actual/Actual (ISDA)', 0.20821918, 8),
        # (date(2018, 12, 31), date(2019, 1, 1), 'Actual/Actual (ISDA)', 1 / 365, 8),
        # (date(1994, 6, 30), date(1997, 6, 30), 'Actual/Actual (ISDA)', 3.0, 8),
        # (date(1994, 2, 10), date(1994, 6, 30), 'Actual/Actual (ISDA)', 140 / 365, 8)
    ]
    for first, second, day_count, expected, ndigits in params:
        actual = years(day_count, first, second)
        assert round(actual, ndigits) == round(expected, ndigits)
