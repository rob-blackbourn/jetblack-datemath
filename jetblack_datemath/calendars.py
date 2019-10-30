"""Calendars"""

from abc import ABCMeta, abstractmethod
import datetime
from typing import List, Dict

# from .arithmetic import date
from .weekdays import DayOfWeek


class AbstractCalendar(metaclass=ABCMeta):
    """Abstract calendar"""

    @abstractmethod
    def is_weekend(self, target_date: datetime.date) -> bool:
        """If a weekend true, otherwise false

        :param target_date: The target date
        :type target_date: date
        :return: True if a weekend, otherwise false
        :rtype: bool
        """

    @abstractmethod
    def is_holiday(self, target_date: datetime.date) -> bool:
        """If a holiday true, otherwise false

        :param target_date: The target date
        :type target_date: date
        :return: True if a weekend, otherwise false.
        :rtype: bool
        """

    @abstractmethod
    def is_business_day(self, target_date: datetime.date) -> bool:
        """True if a business day, otherwise false

        :param target_date: The target date
        :type target_date: date
        :return: True is a business day, otherwise false.
        :rtype: bool
        """


class AbstractWeekendCalendar(AbstractCalendar):
    """AbstractWeekendCalendar"""

    def __init__(self, weekends: List[DayOfWeek]) -> None:
        """Initialise the calendAR

        :param weekends: The days of the week that are holidays
        :type weekends: List[DayOfWeek]
        """
        self.weekends = weekends

    @abstractmethod
    def is_holiday(self, target_date: datetime.date) -> bool:
        ...

    def is_weekend(self, target_date: datetime.date) -> bool:
        return target_date.weekday() in self.weekends

    def is_business_day(self, target_date: datetime.date) -> bool:
        return not (self.is_weekend(target_date) or self.is_holiday(target_date))


class SimpleCalendar(AbstractWeekendCalendar):
    """SimpleCalendar"""

    def __init__(self, weekends: List[DayOfWeek], holidays: List[datetime.date]) -> None:
        super().__init__(weekends)
        self.holidays = holidays

    def is_holiday(self, target_date: datetime.date) -> bool:
        return target_date in self.holidays


class YearlyCalendar(AbstractWeekendCalendar):
    """YearlyCalendar"""

    def __init__(self, weekends: List[DayOfWeek]) -> None:
        super().__init__(weekends)
        self._holidays: Dict[int, Dict[datetime.date, str]] = {}

    def is_holiday(self, target_date: datetime.date) -> bool:
        if target_date.year not in self._holidays:
            self._holidays[target_date.year] = self.fetch_holidays(
                target_date.year)

        return target_date in self._holidays[target_date.year]

    @abstractmethod
    def fetch_holidays(self, year: int) -> Dict[datetime.date, str]:
        """Fetch holidays for a given year

        :param year: The year
        :type year: int
        :return: Holidays for that year
        :rtype: Dict[date, str]
        """
