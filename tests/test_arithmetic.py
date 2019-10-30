"""Tests"""

from datetime import date
import jetblack_datemath.arithmetic as datemath
from jetblack_datemath.daterules import BusinessDayConvention
from jetblack_datemath.calendars import SimpleCalendar
from jetblack_datemath.weekdays import DayOfWeek


def test_days_in_month():
    """Test days_in_month"""
    assert datemath.days_in_month(2009, 1) == 31, "28 days in January."
    assert datemath.days_in_month(
        2009, 2) == 28, "28 days in February in a non leap year."
    assert datemath.days_in_month(2009, 3) == 31, "There are 31 days in March."
    assert datemath.days_in_month(2009, 4) == 30, "There are 30 days in April."
    assert datemath.days_in_month(2009, 5) == 31, "There are 31 days in May."
    assert datemath.days_in_month(2009, 6) == 30, "There are 30 days in June."
    assert datemath.days_in_month(2009, 7) == 31, "There are 31 days in July."
    assert datemath.days_in_month(2009, 8) == 31, "There are 31 days in August."
    assert datemath.days_in_month(2009, 9) == 30, "There are 30 days in September."
    assert datemath.days_in_month(2009, 10) == 31, "There are 31 days in October."
    assert datemath.days_in_month(2009, 11) == 30, "There are 30 days in November."
    assert datemath.days_in_month(2009, 12) == 31, "There are 31 days in December."
    assert datemath.days_in_month(2008, 2) == 29, "There are 29 days in February in a leap year."


def test_is_weekend():
    """Test weekend detection"""
    assert not datemath.WEEKEND_CALENDAR.is_weekend(
        date(2014, 12, 19)
    ), "19 December 2014 was a Friday."
    assert datemath.WEEKEND_CALENDAR.is_weekend(
        date(2014, 12, 20)
    ), "20 December 2014 was a Saturday."
    assert datemath.WEEKEND_CALENDAR.is_weekend(
        date(2014, 12, 21)
    ), "21 December 2014 was a Sunday."
    assert not datemath.WEEKEND_CALENDAR.is_weekend(
        date(2014, 12, 22)
    ), "22 December 2014 was a Monday."


def test_is_end_of_month():
    """Test end of month"""
    assert not datemath.is_end_of_month(
        date(2008, 1, 30)
    ), "30 January is not the end of the month."
    assert datemath.is_end_of_month(
        date(2008, 1, 31)
    ), "31 January is the end of the month."
    assert not datemath.is_end_of_month(
        date(2008, 2, 28)
    ), "28 February 2008 is not the end of the month because it's a leap year."
    assert datemath.is_end_of_month(
        date(2008, 2, 29)
    ), "28 February 2008 is the end of the month because it's a leap year."
    assert datemath.is_end_of_month(
        date(2009, 2, 28)
    ), "28 February 2009 is the end of the month because it's a not leap year."


def test_is_holiday():
    """Test for holidays"""
    cal = SimpleCalendar(
        [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY],
        [date(2014, 12, 25), date(2014, 12, 26)]
    )
    assert cal.is_holiday(
        date(2014, 12, 25)
    ), "Thursday 25 December 2014 is a holiday."
    assert cal.is_holiday(
        date(2014, 12, 26)
    ), "Friday 26 December 2014 is a holiday."
    assert not cal.is_holiday(
        date(2014, 12, 27)
    ), "Saturday 27 December 2014 is not a holiday."


def test_is_business_day():
    """Test for Business days"""
    cal = SimpleCalendar(
        [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY],
        [date(2014, 12, 25), date(2014, 12, 26)]
    )
    assert cal.is_business_day(
        date(2014, 12, 24)
    ), "Wednesday 24 December 2014 is a business day."
    assert not cal.is_business_day(
        date(2014, 12, 25)
    ), "Thursday 25 December 2014 is not a business day."
    assert not cal.is_business_day(
        date(2014, 12, 26)
    ), "Friday 26 December 2014 is not a business day."
    assert not cal.is_business_day(
        date(2014, 12, 27)
    ), "Saturday 27 December 2014 is not a business day."
    assert not cal.is_business_day(
        date(2014, 12, 28)
    ), "Sunday 28 December 2014 is not a business day."
    assert cal.is_business_day(
        date(2014, 12, 29
             )), "Monday 29 December 2014 is a business day."


def test_add_months():
    """Test adding months"""

    # Forward
    assert date(2013, 2, 28) == datemath.add_months(
        date(2012, 11, 30), 3), "Should not roll into March."
    assert date(2013, 4, 28) == datemath.add_months(
        date(2013, 2, 28), 2, False), "Should not go to end of month."
    assert date(2013, 4, 30) == datemath.add_months(
        date(2013, 2, 28), 2, True), "Should go to end of month."
    assert date(2013, 1, 30) == datemath.add_months(
        date(2012, 11, 30), 2, False), "Should not go to end of month."
    assert date(2013, 1, 31) == datemath.add_months(
        date(2012, 11, 30), 2, True), "Should go to end of month."
    # Back
    assert date(2012, 11, 28) == datemath.add_months(
        date(2013, 2, 28), -3, False), "Should not roll into March."
    assert date(2012, 11, 30) == datemath.add_months(
        date(2013, 2, 28), -3, True), "Should go to end of month."
    assert date(2013, 1, 28) == datemath.add_months(
        date(2013, 4, 28), -3, True), "Should not go to end of month."
    assert date(2012, 1, 28) == datemath.add_months(
        date(2013, 4, 28), -15, True), "Should not go to end of month."
    assert date(2013, 4, 30) == datemath.add_months(
        date(2013, 5, 31), -1, True), "Should not stay in May."
    assert date(2013, 4, 30) == datemath.add_months(
        date(2013, 5, 31), -1, False), "Should not stay in May."


def test_easter():
    """Test easter"""
    assert date(2001, 4, 15) == datemath.easter(2001), "Easter 2001"
    assert date(2002, 3, 31) == datemath.easter(2002), "Easter 2002"
    assert date(2003, 4, 20) == datemath.easter(2003), "Easter 2003"
    assert date(2004, 4, 11) == datemath.easter(2004), "Easter 2004"
    assert date(2005, 3, 27) == datemath.easter(2005), "Easter 2005"
    assert date(2006, 4, 16) == datemath.easter(2006), "Easter 2006"
    assert date(2007, 4, 8) == datemath.easter(2007), "Easter 2007"
    assert date(2008, 3, 23) == datemath.easter(2008), "Easter 2008"
    assert date(2009, 4, 12) == datemath.easter(2009), "Easter 2009"
    assert date(2010, 4, 4) == datemath.easter(2010), "Easter 2010"
    assert date(2011, 4, 24) == datemath.easter(2011), "Easter 2011"
    assert date(2012, 4, 8) == datemath.easter(2012), "Easter 2012"
    assert date(2013, 3, 31) == datemath.easter(2013), "Easter 2013"
    assert date(2014, 4, 20) == datemath.easter(2014), "Easter 2014"
    assert date(2015, 4, 5) == datemath.easter(2015), "Easter 2015"
    assert date(2016, 3, 27) == datemath.easter(2016), "Easter 2016"
    assert date(2017, 4, 16) == datemath.easter(2017), "Easter 2017"
    assert date(2018, 4, 1) == datemath.easter(2018), "Easter 2018"
    assert date(2019, 4, 21) == datemath.easter(2019), "Easter 2019"
    assert date(2020, 4, 12) == datemath.easter(2020), "Easter 2020"
    assert date(2021, 4, 4) == datemath.easter(2021), "Easter 2021"


def test_add_business_days():
    """Test adding business days"""
    cal = SimpleCalendar(
        [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY],
        [
            date(2015, 1, 1),
            date(2015, 4, 3),
            date(2015, 4, 6),
            date(2015, 5, 1),
            date(2015, 12, 25),
            date(2015, 12, 16)]
    )
    # Forward
    assert date(2015, 1, 8) == datemath.add_business_days(
        date(2015, 1, 1), 5, cal
    ), "Should skip New Years Day."
    assert date(2015, 1, 8) == datemath.add_business_days(
        date(2015, 1, 2), 4, cal
    ), "Nothing to skip."
    assert date(2015, 1, 2) == datemath.add_business_days(
        date(2014, 12, 29), 3, cal
    ), "Nothing to skip."
    # Back
    assert date(2014, 12, 31) == datemath.add_business_days(
        date(2015, 1, 8), -5, cal
    ), "Should skip New Years Day."
    assert date(2015, 1, 2) == datemath.add_business_days(
        date(2015, 1, 8), -4, cal
    ), "Nothing to skip."
    assert date(2014, 12, 29) == datemath.add_business_days(
        date(2015, 1, 2), -3, cal
    ), "Nothing to skip."


def test_nearest_business_day():
    """Test for nearest business day"""
    #              July 2015
    # Su Mo Tu We Th Fr Sa
    #           1  2  3  4
    #  5  6  7  8  9 10 11
    # 12 13 14 15 16 17 18
    # 19 20 21 22 23 24 25
    # 26 27 28 29 30 31
    cal = SimpleCalendar(
        [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY],
        [date(2015, 7, 13)]
    )
    assert date(2015, 7, 3) == datemath.nearest_business_day(
        date(2015, 7, 4), True, cal
    ), "Saturday should roll to Friday"
    assert date(2015, 7, 6) == datemath.nearest_business_day(
        date(2015, 7, 5), True, cal
    ), "Sunday should roll to Monday"
    assert date(2015, 7, 14) == datemath.nearest_business_day(
        date(2015, 7, 12), True, cal
    ), "Sunday should prefer to roll to Tuesday"
    assert date(2015, 7, 10) == datemath.nearest_business_day(
        date(2015, 7, 12), False, cal
    ), "Sunday should prefer to roll to Friday"


def test_add_nth_day_of_week():
    """Test day of week arithmetic"""
    #      June 2015
    # Su Mo Tu We Th Fr Sa
    #     1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 27
    # 28 29 30
    assert date(2015, 6, 1) == datemath.add_nth_day_of_week(
        date(2015, 6, 1), 1, DayOfWeek.MONDAY, False
    ), "The first Monday is the same date."
    assert date(2015, 6, 8) == datemath.add_nth_day_of_week(
        date(2015, 6, 1), 1, DayOfWeek.MONDAY, True
    ), "When strictly different go to the next week."
    assert date(2015, 6, 2) == datemath.add_nth_day_of_week(
        date(2015, 6, 1), 1, DayOfWeek.TUESDAY, False
    ), "The first Tuesday is the next date."
    assert date(2015, 6, 2) == datemath.add_nth_day_of_week(
        date(2015, 6, 1), 1, DayOfWeek.TUESDAY, True
    ), "Strictly different should make no difference."
    assert date(2015, 6, 17) == datemath.add_nth_day_of_week(
        date(2015, 6, 1), 3, DayOfWeek.WEDNESDAY, False
    ), "Third Wednesday."
    assert date(2015, 6, 30) == datemath.add_nth_day_of_week(
        date(2015, 6, 30), -1, DayOfWeek.TUESDAY, False
    ), "The last Tuesday is the same date."
    assert date(2015, 6, 23) == datemath.add_nth_day_of_week(
        date(2015, 6, 30), -1, DayOfWeek.TUESDAY, True
    ), "Skip the start date as it's a Tuesday."
    assert date(2015, 6, 10) == datemath.add_nth_day_of_week(
        date(2015, 6, 30), -3, DayOfWeek.WEDNESDAY, True
    ), "Third Wednesday from the end of the month.."


def test_adjust():
    """Test date adjustment"""
    weekends = [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY]
    holidays = [
        date(2015, 1, 1),
        date(2015, 4, 3),
        date(2015, 4, 6),
        date(2015, 5, 1),
        date(2015, 12, 25),
        date(2015, 12, 16)
    ]
    cal = SimpleCalendar(weekends, holidays)

    jan_first = date(2015, 1, 1)
    jan_second = date(2015, 1, 2)

    # BusinessDayConvention.none
    assert datemath.adjust(
        jan_first, BusinessDayConvention.NONE, True, cal
    ) == jan_first, "No adjustment."

    # BusinessDayConvention.following
    assert datemath.adjust(
        jan_first, BusinessDayConvention.FOLLOWING, True, cal
    ) == jan_second, "Adjusted to January 2."
