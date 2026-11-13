import csv

from supplier import Supplier
from inventory import Inventory
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Reads products from a CSV file, creates each one through ProductFactory,
    and adds it to the inventory. One bad row is reported and skipped."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                     # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity),
                                                    supplier)
                except ValueError as error:
                    print(f"Skipped row {line_number} {row}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipped row {line_number}: product ID {product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
