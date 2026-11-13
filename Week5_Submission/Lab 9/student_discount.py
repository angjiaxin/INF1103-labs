from discount_strategy import DiscountStrategy

STUDENT_DISCOUNT_RATE: float = 0.05   # 5% off for students


class StudentDiscount(DiscountStrategy):
    """Fourth strategy, added WITHOUT changing Order (Open/Closed Principle)."""

    def apply(self, total: float) -> float:
        return total * (1 - STUDENT_DISCOUNT_RATE)
