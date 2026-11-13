import unittest

from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


class TestDiscountStrategies(unittest.TestCase):

    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount_takes_percentage_off(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_applies_at_or_above_threshold(self):
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230)
        self.assertEqual(bulk.apply(200), 180)   # exactly on the threshold

    def test_bulk_discount_not_applied_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_takes_five_percent_off(self):
        self.assertAlmostEqual(StudentDiscount().apply(200), 190)

    def test_invalid_percentage_is_rejected(self):
        for bad in (0, -10, 150):
            with self.assertRaises(ValueError):
                PercentageDiscount(bad)

    def test_invalid_bulk_discount_is_rejected(self):
        with self.assertRaises(ValueError):
            BulkDiscount(200, 0)
        with self.assertRaises(ValueError):
            BulkDiscount(10, 20)   # discount bigger than the threshold


if __name__ == "__main__":
    unittest.main()
