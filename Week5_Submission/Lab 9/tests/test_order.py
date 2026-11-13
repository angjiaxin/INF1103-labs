import inspect
import re
import unittest

import order as order_module
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from tests.helpers import make_physical, make_digital


def make_order_of_250(discount: DiscountStrategy | None = None) -> Order:
    """2 x $100 + 1 x $50 = $250"""
    order = Order("ORD001", discount)
    order.add_order_line(make_physical(price=100.00), 2)
    order.add_order_line(make_digital(price=50.00), 1)
    return order


class TestOrderWithStrategy(unittest.TestCase):

    def test_default_strategy_is_no_discount(self):
        order = make_order_of_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_total_uses_bulk_discount(self):
        self.assertEqual(make_order_of_250(BulkDiscount(200, 20)).calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        class TenDollarsOff(DiscountStrategy):      # brand new strategy, defined only here
            def apply(self, total: float) -> float:
                return total - 10

        self.assertEqual(make_order_of_250(TenDollarsOff()).calculate_total(), 240)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        order_1 = make_order_of_250(shared)
        order_2 = make_order_of_250(shared)
        self.assertIs(order_1.get_discount(), order_2.get_discount())

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(order_module)
        # Order never mentions the concrete discounts (NoDiscount is only the default)
        for name in ("PercentageDiscount", "BulkDiscount", "StudentDiscount", "discount_type"):
            self.assertNotIn(name, source)
        self.assertIsNone(re.search(r"^\s*elif\b", source, re.MULTILINE))  # no elif statements
        self.assertNotIn("if", inspect.getsource(Order.calculate_total))

    def test_removing_a_line_updates_total(self):
        order = make_order_of_250()
        order.remove_order_line("D001")
        self.assertEqual(order.calculate_total(), 200)


if __name__ == "__main__":
    unittest.main()
