from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) = $20 off orders of $200 or more."""

    def __init__(self, threshold: float, amount: float):
        # Validation: the strategy protects its own rules
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        if threshold < amount:
            raise ValueError("Threshold must be at least the discount amount.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total
