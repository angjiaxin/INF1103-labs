

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------
heading("SECTION 2: ASSOCIATION (Supplier and Product)")

supplier = Supplier("SUP001", "TechSource Pte Ltd", "sales@techsource.sg")
guitar = PhysicalProduct("P001", "Guitar", 350.00, 10, supplier, 3.5)
antivirus = DigitalProduct("D001", "Antivirus", 49.90, 100, supplier, 850)

print("Supplier information through each Product:")
guitar.get_supplier().display_information()
antivirus.get_supplier().display_information()

print("\nSupplier and Product are separate objects:")
print("guitar is supplier?               ", guitar is supplier)
print("Both products share ONE supplier? ", guitar.get_supplier() is antivirus.get_supplier())

print("\nPREDICT FIRST: del supplier, then display supplier through the products")
del supplier
guitar.get_supplier().display_information()
antivirus.get_supplier().display_information()
print("-> Still works: 'del' only removed the variable name, not the object.")
print("   Each Product still holds its own reference to the Supplier.")


# ---------------------------------------------------------------
heading("SECTION 3: AGGREGATION (Inventory and Product)")

supplier_b = Supplier("SUP002", "Melody Music", "hello@melody.sg")
piano = PhysicalProduct("P002", "Piano", 2500.00, 2, supplier_b, 150)   # created BEFORE any inventory
print("Product created before any Inventory:")
piano.display_information()

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(piano)
print("\nAdded to Inventory A. Found in A?", inventory_a.find_product("P002") is not None)

print("\nPREDICT FIRST: will the Product still work after removing it from Inventory A?")
inventory_a.remove_product("P002")
print("Found in A after removal?", inventory_a.find_product("P002") is not None)
print("Product still usable:")
piano.update_stock(3)
piano.display_information()

inventory_b.add_product(piano)
print("\nSame object added to Inventory B. Same object?", inventory_b.find_product("P002") is piano)
print("-> Removing it from A only removed the reference. The Product was never destroyed.")


# ---------------------------------------------------------------
heading("SECTION 4: COMPOSITION (Order and OrderLine)")

order_1 = Order("ORD001")
order_1.add_order_line(guitar, 2)       # Order creates the OrderLine itself
order_1.add_order_line(antivirus, 3)
order_1.add_order_line(piano, 1)
order_1.display_information()

print("\nPREDICT FIRST: same Product added to two different Orders")
order_2 = Order("ORD002")
order_2.add_order_line(guitar, 1)

line_in_order_1 = order_1.get_order_lines()[0]
line_in_order_2 = order_2.get_order_lines()[0]
print("Same OrderLine object?      ", line_in_order_1 is line_in_order_2)
print("Same Product object?        ", line_in_order_1.get_product() is line_in_order_2.get_product())
print("OrderLine ids:", id(line_in_order_1), id(line_in_order_2))
print("Product ids:  ", id(line_in_order_1.get_product()), id(line_in_order_2.get_product()))
print("-> 2 OrderLine objects (one per Order), but only 1 Product object.")

print("\nRemove the Piano line from Order ORD001:")
order_1.remove_order_line("P002")
order_1.display_information()
print("Piano still exists in Inventory B?", inventory_b.find_product("P002") is piano)
print("-> The OrderLine was discarded by its Order; the Product was not affected.")


# ---------------------------------------------------------------
heading("SECTION 6: LISKOV SUBSTITUTION PRINCIPLE")


def show_product_details(product: Product) -> None:
    """Accepts ANY Product. It never checks which subclass it was given."""
    product.display_information()
    print(product.get_fulfilment_info())


print("show_product_details() with a PhysicalProduct:")
show_product_details(guitar)
print("\nshow_product_details() with a DigitalProduct:")
show_product_details(antivirus)

print("\nExpectation from Product: update_stock() ADDS the quantity to stock.")
for product in (guitar, antivirus):
    before = product.get_stock()
    product.update_stock(5)
    print(f"{product.get_name()}: {before} + 5 = {product.get_stock()}")
print("-> Both subclasses keep the same meaning, so either can replace Product.")


# ---------------------------------------------------------------
heading("SECTION 7: POLYMORPHISM (one loop, no isinstance)")

shop = Inventory()
shop.add_product(guitar)
shop.add_product(antivirus)
shop.add_product(piano)

print("PREDICT FIRST: what will each product print for get_fulfilment_info()?\n")
for product in shop.get_products():
    product.display_information()
    print("   ", product.get_fulfilment_info())

print("\nInventory.display_all() works with both types too:")
shop.display_all()