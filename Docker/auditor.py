print("--------------")
print("Welcome to Smart Inventory Auditor")
print("--------------")


inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to exit): ")

    if stock.lower() == "quit":
        break

    elif not stock.isdigit():
        print("Error: Invalid input. Please enter an integer.")
        failed_entries += 1
        continue

    stock = int(stock)

    if stock < 0:
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    inventory += stock

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)