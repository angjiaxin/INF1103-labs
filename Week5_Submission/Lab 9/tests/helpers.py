"""Shared test objects, so each test file builds products the same way."""

from supplier import Supplier
from product import Product
from product_factory import ProductFactory


def make_supplier() -> Supplier:
    return Supplier("SUP001", "TechSource Pte Ltd", "sales@techsource.sg")


def make_physical(product_id: str = "P001", price: float = 100.00) -> Product:
    return ProductFactory.create("physical", product_id, "Desk Lamp", price, 10,
                                 make_supplier(), weight=2.0)


def make_digital(product_id: str = "D001", price: float = 50.00) -> Product:
    return ProductFactory.create("digital", product_id, "Photo Editor", price, 100,
                                 make_supplier(), download_size=850)
