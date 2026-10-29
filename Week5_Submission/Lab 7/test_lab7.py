"""Tests for each section of Lab 7. Run with:  python test_lab7.py"""

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped

print("=== 1 & 2. Inheritance + method overriding ===")
guitar = PhysicalProduct("P001", "Guitar", 350.00, 10, 3.5)
os_licence = DigitalProduct("D001", "Operating System", 199.00, 100, 4500)
guitar.display_information()       # parent info + weight
os_licence.display_information()   # parent info + download size

print("\n=== 3.2 Abstract method implemented by both children ===")
print("Guitar:", guitar.get_fulfilment_info())
print("OS:    ", os_licence.get_fulfilment_info())

print("\n=== 3.3 Try to create a Product directly ===")
try:
    generic = Product("X001", "Generic", 1.00, 1)
except TypeError as error:
    print("TypeError:", error)

print("\n=== 4.2 Shipping cost for different weights ===")
for weight in (0.5, 3.5, 20):
    item = PhysicalProduct("T001", "Test Item", 10.00, 1, weight)
    print(f"{weight} kg -> ${item.calculate_shipping_cost():.2f}")

print("\n=== 4.2 Which products can be shipped? ===")
print("Guitar is CanBeShipped:", isinstance(guitar, CanBeShipped))
print("OS is CanBeShipped:    ", isinstance(os_licence, CanBeShipped))