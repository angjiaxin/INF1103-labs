import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from tests.helpers import make_supplier


class TestProductFactory(unittest.TestCase):

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10,
                                        make_supplier(), weight=2.0)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 2.0)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100,
                                        make_supplier(), download_size=850)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 850)

    def test_product_type_ignores_case_and_spaces(self):
        product = ProductFactory.create("  Physical ", "P002", "Chair", 80.00, 3,
                                        make_supplier())
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_product_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5,
                                  make_supplier())
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()
