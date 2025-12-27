from abc import ABCMeta, abstractmethod
from datetime import date


class DayCount(metaclass=ABCMeta):

    @property
    @abstractmethod
    def names(self) -> list[str]:
        ...

    @abstractmethod
    def days(self, start: date, end: date) -> int:
        ...

    @abstractmethod
    def years(self, start: date, end: date, ref_start: date, ref_end: date) -> float:
        ...
