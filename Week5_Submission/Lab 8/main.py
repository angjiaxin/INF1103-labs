import os
import json

from supplier import Supplier
from product import Product
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from order import Order

FILENAME: str = 'inventory.json'
OVERSTOCK_LIMIT: int = 500

# Used for products saved before Lab 8, which have no supplier yet
DEFAULT_SUPPLIER_DATA: dict = {
    "supplier_id": "SUP000",
    "name": "Unknown Supplier",
    "contact_email": "unknown@example.com"
}


# ---------------- Input helpers (main program's job) ----------------

def get_valid_input(prompt: str) -> int | None:
    """Returns a non-negative int, or None if the input is invalid."""
    stock = input(prompt).strip()
    if not stock.isdigit():
        print("Error: Invalid input. Please enter a non-negative integer.")
        return None
    return int(stock)


def get_valid_number(prompt: str) -> float | None:
    """Returns a non-negative float, or None if the input is invalid.
    Used for price, weight and download size."""
    text = input(prompt).strip()
    try:
        value = float(text)
    except ValueError:
        print("Error: Invalid number. Please enter a number.")
        return None
    if value < 0:
        print("Error: Value cannot be negative.")
        return None
    return value


# ---------------- File handling ----------------

def get_or_create_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Reuses the same Supplier object for the same supplier ID,
    so products from one supplier all share ONE Supplier (association)."""
    supplier_id = data["supplier_id"].upper()
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]


def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    """Uses the saved 'type' to rebuild the correct subclass."""
    supplier = get_or_create_supplier(item.get("supplier", DEFAULT_SUPPLIER_DATA), suppliers)
    product_type = item.get("type", "physical")  # Lab 6 data has no type: treat as physical

    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["stock"],
                              supplier, item["download_size"], item.get("history"))

    return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"],
                           supplier, item.get("weight", 0.0), item.get("history"))


def load_inventory(filename: str, suppliers: dict[str, Supplier]) -> Inventory:
    """Builds an Inventory object from the JSON file (or an empty one)."""
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found.")
        print("Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(create_product_from_dict(item, suppliers))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, KeyError):
        print("Error: File is unreadable. Starting with an empty inventory.")
        inventory = Inventory()
        suppliers.clear()

    return inventory


def save_inventory(filename: str, inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully!")


# ---------------- Menu actions ----------------

def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """Uses an existing Supplier if the ID is known, otherwise creates a new one.
    The Supplier is created FIRST, then given to the Product."""
    supplier_id = input("Supplier ID: ").strip().upper()
    if supplier_id == "":
        print("Error: Supplier ID cannot be empty.")
        return None

    if supplier_id in suppliers:
        supplier = suppliers[supplier_id]
        print(f"Using existing supplier: {supplier.get_name()}")
        return supplier

    print("New supplier.")
    name = input("Supplier Name: ").strip()
    email = input("Supplier Email: ").strip()
    if name == "" or email == "":
        print("Error: Supplier name and email cannot be empty.")
        return None

    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier


def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type (1-2): ").strip()
    if product_type not in ("1", "2"):
        print("Error: Please enter 1 or 2.")
        return

    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print("Error: Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Error: Product name cannot be empty.")
        return

    price = get_valid_number("Price: ")
    if price is None:
        return

    stock = get_valid_input("Stock Quantity: ")
    if stock is None:
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product: Product
    if product_type == "1":
        weight = get_valid_number("Weight (kg): ")
        if weight is None:
            return
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_valid_number("Download Size (MB): ")
        if download_size is None:
            return
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Error: Product not found.")
        return

    print(f"Current Stock: {product.get_stock()}")
    amount = get_valid_input("Delivery Quantity: ")
    if amount is None:
        return

    product.update_stock(amount)          # the Product changes its own stock
    tax = product.calculate_tax(amount)

    print("\nStock updated successfully!")
    print(f"New Stock: {product.get_stock()} | Tax on this delivery: {tax:.2f}")

    if product.is_overstocked(OVERSTOCK_LIMIT):
        print(f"ALERT: Overstock! {product.get_name()} exceeds {OVERSTOCK_LIMIT} units.")


def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    term = input("Enter Product ID or Name: ").strip()
    matches = inventory.search_product(term)

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
    product_id = input("Product ID: ").strip()
    removed = inventory.remove_product(product_id)
    if removed is None:
        print("Error: Product not found.")
        return
    print(f"{removed.get_name()} removed from the inventory.")


def create_order_menu(inventory: Inventory) -> None:
    print("\nCreate Order")
    order_id = input("Order ID: ").strip().upper()
    if order_id == "":
        print("Error: Order ID cannot be empty.")
        return

    order = Order(order_id)
    print("Add items to the order. Leave Product ID empty to finish.")

    while True:
        product_id = input("\nProduct ID: ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Error: Product not found.")
            continue
        quantity = get_valid_input("Quantity: ")
        if quantity is None or quantity == 0:
            print("Error: Quantity must be at least 1.")
            continue
        order.add_order_line(product, quantity)   # the Order creates the OrderLine
        print(f"Added {quantity} x {product.get_name()}.")

    order.display_information()


# ---------------- Menu system ----------------

def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
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
            save_inventory(FILENAME, inventory)
        elif choice == "8":
            save_inventory(FILENAME, inventory)
            print("Goodbye!")
            break
        else:
            print("Error: Invalid option. Please enter 1-8.")


if __name__ == "__main__":
    main()