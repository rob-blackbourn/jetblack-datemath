from abc import ABCMeta, abstractmethod
from datetime import date


class DayCount(metaclass=ABCMeta):

    @property
    @abstractmethod
    def names(self) -> list[str]:
        ...

    @abstractmethod
    def days(
            self,
            date1: date,
            date2: date,
            maturity: date,
            is_eom: bool
    ) -> int:
        ...

    @abstractmethod
    def years(
            self,
            date1: date,
            date2: date,
            ref_date1: date,
            ref_date2: date,
            maturity: date,
            is_eom: bool
    ) -> float:
        ...
