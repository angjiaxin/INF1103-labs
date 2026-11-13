from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: every discount provides the same apply() method.
    Order only calls apply(); it never needs to know which discount it has."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass
