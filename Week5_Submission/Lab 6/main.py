import os
import json

from product import Product
from inventory import Inventory

FILENAME = 'inventory.json'
OVERSTOCK_LIMIT = 500


# ---------------- Input helpers (main program's job) ----------------

def get_valid_input(prompt):
    """Returns a non-negative int, or None if the input is invalid."""
    stock = input(prompt).strip()
    if not stock.isdigit():
        print("Error: Invalid input. Please enter a non-negative integer.")
        return None
    return int(stock)


def get_valid_price(prompt):
    """Returns a non-negative float, or None if the input is invalid."""
    price = input(prompt).strip()
    try:
        value = float(price)
    except ValueError:
        print("Error: Invalid price. Please enter a number.")
        return None
    if value < 0:
        print("Error: Price cannot be negative.")
        return None
    return value


# ---------------- File handling ----------------

def load_inventory(filename):
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
            product = Product(item["id"], item["name"], item["price"],
                              item["stock"], item.get("history"))
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, KeyError):
        print("Error: File is unreadable. Starting with an empty inventory.")
        inventory = Inventory()

    return inventory


def save_inventory(filename, inventory):
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully!")


# ---------------- Menu actions ----------------

def add_product_menu(inventory):
    print("\nAdd New Product")
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

    price = get_valid_price("Price: ")
    if price is None:
        return

    stock = get_valid_input("Stock Quantity: ")
    if stock is None:
        return

    inventory.add_product(Product(product_id, name, price, stock))
    print("\nProduct added successfully!")


def update_stock_menu(inventory):
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


def search_product_menu(inventory):
    print("\nSearch Product")
    term = input("Enter Product ID or Name: ").strip()
    matches = inventory.search_product(term)

    if not matches:
        print("No matching product found.")
        return

    for product in matches:
        product.display_information()
        print(f"Transaction History: {product.get_history()}")


# ---------------- Menu system ----------------

def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = load_inventory(FILENAME)

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(FILENAME, inventory)
        elif choice == "6":
            save_inventory(FILENAME, inventory)
            print("Goodbye!")
            break
        else:
            print("Error: Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()