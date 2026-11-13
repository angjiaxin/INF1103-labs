"""Walks through each 'Predict first' in Lab 9. Run with:  python demo_lab9.py

The LAST section deliberately does NOT catch an exception, so the program
crashes on purpose to show what an uncaught ValueError looks like (3.2)."""

from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from product_factory import ProductFactory
from product_loader import load_products
from order import Order
from bulk_discount import BulkDiscount
from percentage_discount import PercentageDiscount
from student_discount import StudentDiscount
from input_helpers import get_positive_float


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


supplier = Supplier("SUP001", "TechSource Pte Ltd", "sales@techsource.sg")

# ---------------------------------------------------------------
heading("2.3 PREDICT FIRST: order of $250 with BulkDiscount(200, 20)")
chair = ProductFactory.create("physical", "P010", "Office Chair", 100.00, 10, supplier, weight=8)
editor = ProductFactory.create("digital", "D010", "Photo Editor", 50.00, 100, supplier,
                               download_size=850)

order = Order("ORD001", BulkDiscount(200, 20))
order.add_order_line(chair, 2)      # 2 x 100 = 200
order.add_order_line(editor, 1)     # 1 x 50  =  50
print(f"Subtotal: ${order.calculate_subtotal():.2f}")
print(f"With BulkDiscount(200, 20):  ${order.calculate_total():.2f}")

order.set_discount(PercentageDiscount(10))
print(f"After set_discount(PercentageDiscount(10)):  ${order.calculate_total():.2f}")

# ---------------------------------------------------------------
heading("2.4 New StudentDiscount strategy, Order NOT changed")
order.set_discount(StudentDiscount())
order.display_information()

shared = PercentageDiscount(10)
order_a = Order("ORD002", shared)
order_b = Order("ORD003", shared)
print("\nTwo orders share the same PercentageDiscount object?",
      order_a.get_discount() is order_b.get_discount())

# ---------------------------------------------------------------
heading("5.1 PREDICT FIRST: user types abc, then -5, then 12.50")
typed = iter(["abc", "-5", "12.50"])


def fake_input(prompt: str) -> str:
    answer = next(typed)
    print(f"{prompt}{answer}")          # show what the user 'typed'
    return answer


with patch("builtins.input", side_effect=fake_input):
    price = get_positive_float("Price: ")
print(f"Returned value: {price}")

# ---------------------------------------------------------------
heading("5.2 PREDICT FIRST: load products.csv")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all()

heading("5.2 PREDICT FIRST: products.csv renamed / missing")
load_products("products_renamed.csv", Inventory(), supplier)

# ---------------------------------------------------------------
heading("3.2 PREDICT FIRST: ProductFactory.create('service', ...) with NOTHING catching it")
print("The program will now crash on purpose:\n")
ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
print("This line never runs.")
