import json

from supplier import Supplier
from product import Product
from inventory import Inventory
from product_factory import ProductFactory
from product_loader import load_products
from can_be_shipped import CanBeShipped
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount
from input_helpers import (get_positive_float, get_non_negative_float,
                           get_non_negative_int, get_positive_int,
                           get_non_empty_text, get_choice)

FILENAME: str = 'inventory.json'
PRODUCTS_CSV: str = 'products.csv'
OVERSTOCK_LIMIT: int = 500

# Used for products saved before Lab 8, which have no supplier yet
DEFAULT_SUPPLIER_DATA: dict = {
    "supplier_id": "SUP000",
    "name": "Unknown Supplier",
    "contact_email": "unknown@example.com"
}


# ---------------- File handling ----------------

def get_or_create_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Reuses the same Supplier object for the same supplier ID,
    so products from one supplier all share ONE Supplier (association)."""
    supplier_id = data["supplier_id"].upper()
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]


def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    """Rebuilds a saved product through the factory (no direct creation here)."""
    supplier = get_or_create_supplier(item.get("supplier", DEFAULT_SUPPLIER_DATA), suppliers)
    return ProductFactory.create(item.get("type", "physical"),   # old data: physical
                                 item["id"], item["name"], item["price"], item["stock"],
                                 supplier,
                                 weight=item.get("weight", 0.0),
                                 download_size=item.get("download_size", 0.0),
                                 history=item.get("history"))


def load_inventory(filename: str, suppliers: dict[str, Supplier]) -> Inventory:
    """Builds an Inventory from the JSON file. A missing or broken file does not
    crash the program, and one bad product is skipped instead of stopping the load."""
    inventory = Inventory()
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory.")
    except json.JSONDecodeError:
        print(f"{filename} is unreadable. Starting with an empty inventory.")
    else:
        for item in data:
            try:
                inventory.add_product(create_product_from_dict(item, suppliers))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipped a saved product with bad data: {error}")
        print(f"Inventory loaded: {len(inventory.get_products())} products.")
    return inventory


def save_inventory(filename: str, inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except OSError:
        print("Error: could not save the inventory file.")
    else:
        print("Inventory saved successfully!")


# ---------------- Menu actions ----------------

def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    """Uses an existing Supplier if the ID is known, otherwise creates a new one."""
    supplier_id = get_non_empty_text("Supplier ID: ").upper()
    if supplier_id in suppliers:
        supplier = suppliers[supplier_id]
        print(f"Using existing supplier: {supplier.get_name()}")
        return supplier

    print("New supplier.")
    name = get_non_empty_text("Supplier Name: ")
    email = get_non_empty_text("Supplier Email: ")
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier


def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = "physical" if get_choice("Choose product type (1-2): ", ("1", "2")) == "1" \
        else "digital"

    product_id = get_non_empty_text("Product ID: ").upper()
    if inventory.find_product(product_id) is not None:
        print("Error: Product ID already exists.")
        return

    name = get_non_empty_text("Product Name: ")
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    supplier = choose_supplier(suppliers)

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_non_negative_float("Weight (kg): ")
    else:
        download_size = get_non_negative_float("Download Size (MB): ")

    product = ProductFactory.create(product_type, product_id, name, price, stock,
                                    supplier, weight=weight, download_size=download_size)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(get_non_empty_text("Product ID: "))
    if product is None:
        print("Error: Product not found.")
        return

    print(f"Current Stock: {product.get_stock()}")
    amount = get_non_negative_int("Delivery Quantity: ")
    product.update_stock(amount)          # the Product changes its own stock
    tax = product.calculate_tax(amount)

    print("\nStock updated successfully!")
    print(f"New Stock: {product.get_stock()} | Tax on this delivery: {tax:.2f}")

    if product.is_overstocked(OVERSTOCK_LIMIT):
        print(f"ALERT: Overstock! {product.get_name()} exceeds {OVERSTOCK_LIMIT} units.")


def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    matches = inventory.search_product(get_non_empty_text("Enter Product ID or Name: "))

    if not matches:
        print("No matching product found.")
        return

    for product in matches:
        product.display_information()
        print(f"    Fulfilment: {product.get_fulfilment_info()}")
        # Interface check: only products that signed the CanBeShipped contract
        # have a shipping cost (this checks the interface, not a subclass)
        if isinstance(product, CanBeShipped):
            print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print("    ", end="")
        product.get_supplier().display_information()
        print(f"    Transaction History: {product.get_history()}")


def remove_product_menu(inventory: Inventory) -> None:
    print("\nRemove Product")
    removed = inventory.remove_product(get_non_empty_text("Product ID: "))
    if removed is None:
        print("Error: Product not found.")
        return
    print(f"{removed.get_name()} removed from the inventory.")


def choose_discount() -> DiscountStrategy:
    """Lets the user pick a strategy. Order itself never decides the discount."""
    print("\nChoose a discount:")
    print("1. No discount")
    print("2. Percentage discount")
    print("3. Bulk discount ($20 off orders of $200 or more)")
    print("4. Student discount (5% off)")
    choice = get_choice("Enter option (1-4): ", ("1", "2", "3", "4"))

    if choice == "2":
        while True:
            try:
                return PercentageDiscount(get_positive_float("Percentage off: "))
            except ValueError as error:          # e.g. more than 100%
                print(error)
    if choice == "3":
        return BulkDiscount(200, 20)
    if choice == "4":
        return StudentDiscount()
    return NoDiscount()


def create_order_menu(inventory: Inventory) -> None:
    print("\nCreate Order")
    order = Order(get_non_empty_text("Order ID: "))
    print("Add items to the order. Leave Product ID empty to finish.")

    while True:
        product_id = input("\nProduct ID: ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Error: Product not found.")
            continue
        quantity = get_positive_int("Quantity: ")
        order.add_order_line(product, quantity)   # the Order creates the OrderLine
        print(f"Added {quantity} x {product.get_name()}.")

    order.set_discount(choose_discount())         # strategy can be changed later
    order.display_information()


def load_csv_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print(f"\nLoad Products from {PRODUCTS_CSV}")
    print("Which supplier provides these products?")
    supplier = choose_supplier(suppliers)
    load_products(PRODUCTS_CSV, inventory, supplier)


# ---------------- Menu system ----------------

def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Load Products from CSV")
    print("8. Save Inventory")
    print("9. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    suppliers: dict[str, Supplier] = {}
    inventory = load_inventory(FILENAME, suppliers)

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory, suppliers)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            remove_product_menu(inventory)
        elif choice == "6":
            create_order_menu(inventory)
        elif choice == "7":
            load_csv_menu(inventory, suppliers)
        elif choice == "8":
            save_inventory(FILENAME, inventory)
        elif choice == "9":
            save_inventory(FILENAME, inventory)
            print("Goodbye!")
            break
        else:
            print("Error: Invalid option. Please enter 1-9.")


if __name__ == "__main__":
    main()
