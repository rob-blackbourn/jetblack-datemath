from abc import ABCMeta, abstractmethod
from datetime import date


class DayCount(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def days(cls, start: date, end: date) -> int:
        ...

    @classmethod
    @abstractmethod
    def years(cls, start: date, end: date, ref_start: date, ref_end: date) -> float:
        ...
