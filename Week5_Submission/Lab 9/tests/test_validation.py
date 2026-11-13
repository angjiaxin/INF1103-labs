import unittest

from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from tests.helpers import make_supplier, make_physical


class TestValidation(unittest.TestCase):

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -5):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P001", "Lamp", bad_price, 10,
                                      make_supplier())

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 25.00, -1, make_supplier())

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.00, 0,
                                        make_supplier())
        self.assertEqual(product.get_stock(), 0)

    def test_digital_product_keeps_the_same_rules(self):
        # LSP: the subclass must not skip the rules Product sets
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", -1, 10, make_supplier())
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 10.00, -1, make_supplier())

    def test_negative_delivery_is_rejected(self):
        with self.assertRaises(ValueError):
            make_physical().update_stock(-5)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(make_physical(), bad_quantity)

    def test_order_rejects_bad_quantity_through_order_line(self):
        order = Order("ORD001")
        with self.assertRaises(ValueError):
            order.add_order_line(make_physical(), 0)
        self.assertEqual(order.get_order_lines(), [])   # nothing half-added


if __name__ == "__main__":
    unittest.main()
