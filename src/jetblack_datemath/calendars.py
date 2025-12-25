"""Calendars"""

from abc import ABCMeta, abstractmethod
import datetime
from typing import Dict, List, Iterable, override

# from .arithmetic import date
from .weekdays import DayOfWeek


class AbstractCalendar(metaclass=ABCMeta):
    """Abstract calendar"""

    @abstractmethod
    def is_business_day(self, target_date: datetime.date) -> bool:
        """True if a business day, otherwise false

        Args:
            target_date (datetime.date): The target date.

        Returns:
            bool: True if a business day, otherwise false.
        """


class WeekendCalendar(AbstractCalendar):
    """WeekendCalendar"""

    def __init__(self, weekends: Iterable[DayOfWeek]) -> None:
        """Initialise the calendar.

        Args:
            weekends (Iterable[DayOfWeek]): The days of the week that are
                holidays
        """
        self.weekends = set(weekends)

    def is_weekend(self, target_date: datetime.date) -> bool:
        """If a weekend true, otherwise false

        Args:
            target_date (datetime.date): The target date

        Returns:
            bool: True if a weekend, otherwise false
        """
        return target_date.weekday() in self.weekends

    @override
    def is_business_day(self, target_date: datetime.date) -> bool:
        return not self.is_weekend(target_date)


class SimpleCalendar(WeekendCalendar):
    """SimpleCalendar"""

    def __init__(self, weekends: List[DayOfWeek], holidays: List[datetime.date]) -> None:
        super().__init__(weekends)
        self.holidays = holidays

    def is_holiday(self, target_date: datetime.date) -> bool:
        return target_date in self.holidays

    @override
    def is_business_day(self, target_date: datetime.date) -> bool:
        return not (self.is_weekend(target_date) or self.is_holiday(target_date))


class YearlyCalendar(WeekendCalendar):
    """YearlyCalendar"""

    def __init__(self, weekends: List[DayOfWeek]) -> None:
        super().__init__(weekends)
        self._holidays: Dict[int, Dict[datetime.date, str]] = {}

    def is_holiday(self, target_date: datetime.date) -> bool:
        """If a holiday true, otherwise false

        Args:
            target_date (datetime.date): The target date

        Returns:
            bool: True if a holiday, otherwise false.
        """
        if target_date.year not in self._holidays:
            self._holidays[target_date.year] = self.fetch_holidays(
                target_date.year)

        return target_date in self._holidays[target_date.year]

    @abstractmethod
    def fetch_holidays(self, year: int) -> Dict[datetime.date, str]:
        """Fetch holidays for a given year

        Args:
            year (int): The year

        Returns:
            Dict[datetime.date, str]: A dictionary of holiday dates with reasons.
        """
