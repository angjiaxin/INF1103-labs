import os
import json

FILENAME = 'inventory.json'
OVERSTOCK_LIMIT = 500


# ---------------- Input & calculation helpers ----------------

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


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def find_product(inventory, product_id):
    """Returns the product dictionary with this ID, or None."""
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def print_product(product):
    print(f"ID: {product['id']} | Name: {product['name']} | "
          f"Price: ${product['price']:.2f} | Stock: {product['stock']}")

# ---------------- Data persistence ----------------

def load_inventory(filename):
    """Loads the inventory list from JSON if the file exists, else starts empty."""
    if not os.path.exists(filename):
        print(f"{filename} not found.")
        print("Starting with an empty inventory.")
        return []

    print(f"{filename} found.")
    try:
        with open(filename, "r") as f:
            inventory = json.load(f)
        print("Inventory loaded successfully.")
        return inventory
    except json.JSONDecodeError:
        print("Error: File is unreadable. Starting with an empty inventory.")
        return []
# ---------------- Data manipulation ----------------

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 45)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print_product(product)
    print("-" * 45)


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):
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

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "history": [stock]
    })
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Error: Product not found.")
        return

    print(f"Current Stock: {product['stock']}")
    amount = get_valid_input("Delivery Quantity: ")
    if amount is None:
        return

    product["stock"] = process_delivery(product["stock"], amount)
    product["history"].append(amount)
    tax = calculate_tax(amount)

    print("\nStock updated successfully!")
    print(f"New Stock: {product['stock']} | Tax on this delivery: {tax:.2f}")

    if product["stock"] > OVERSTOCK_LIMIT:
        print(f"ALERT: Overstock! {product['name']} exceeds {OVERSTOCK_LIMIT} units.")


def search_product(inventory):
    print("\nSearch Product")
    term = input("Enter Product ID or Name: ").strip().lower()
    matches = [p for p in inventory
               if term == p["id"].lower() or term in p["name"].lower()]

    if not matches:
        print("No matching product found.")
        return

    for product in matches:
        print_product(product)
        print(f"Transaction History: {product['history']}")


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
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Save not available yet.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Error: Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()