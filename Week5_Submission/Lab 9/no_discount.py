from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged. Used when an order has no discount."""

    def apply(self, total: float) -> float:
        return total
