import os

print("--------------")
print("Welcome to Smart Inventory Auditor")
print("--------------")

FILENAME = 'data/inventory.txt'
 
 
def get_valid_input():
    stock = input("Enter stock quantity (or 'quit' to exit): ")
 
    if stock.lower() == "quit":
        return "quit"
 
    if not stock.isdigit():
        print("Error: Invalid input. Please enter an integer.")
        return None
 
    value = int(stock)
 
    if value < 0:
        print("Error: Negative numbers are not allowed.")
        return None
 
    return value

def process_delivery(current_total, new_value):
    return current_total + new_value
 
 
def calculate_tax(amount):
    return amount * 0.10
 
 
def generate_report(total_deliveries, failed_attempts):
    """Prints the final summary."""
    print("--------------")
    print("Total Deliveries Processed:", total_deliveries)
    print("Number of Failed/Rejected Entries:", failed_attempts)
 
def load_inventory(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        total = int(lines[0])
        history = [int(line) for line in lines[1:]]
        return total, history
    except FileNotFoundError:
        return 0, []

def save_inventory(filename, total, history):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"{total}\n")
        for amount in history:
            f.write(f"{amount}\n")

def main():
    inventory, history = load_inventory(FILENAME)
    deliveries_processed = 0
    failed_entries = 0
    total_tax_collected = 0.0
 
    while True:
        result = get_valid_input()
 
        if result == "quit":
            break
 
        if result is None:
            failed_entries += 1
            continue
 
        inventory = process_delivery(inventory, result)
        history.append(result)
        tax = calculate_tax(result)
        total_tax_collected += tax
        deliveries_processed += 1
 
        print(f"  -> Delivery accepted. Tax on this delivery: {tax:.2f}")
 
        if inventory > 500:
            print("ALERT: Overstock! Inventory exceeds 500 units.")
            break

    save_inventory(FILENAME, inventory, history)
    generate_report(deliveries_processed, failed_entries)
    print(f"Total Units in Inventory: {inventory}")
    print(f"Total Tax Collected: {total_tax_collected:.2f}")
 
 
if __name__ == "__main__":
    main()
 