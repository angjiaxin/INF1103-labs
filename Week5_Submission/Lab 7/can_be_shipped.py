from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: any class that 'can be shipped'
    must provide a way to calculate its shipping cost.
    No attributes and no implementation details live here."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass