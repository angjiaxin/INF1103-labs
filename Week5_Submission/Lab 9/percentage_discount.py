from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) = 10% off."""

    def __init__(self, percentage: float):
        # Validation: the strategy protects its own rule
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)
