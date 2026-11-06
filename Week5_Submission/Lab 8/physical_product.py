from product import Product
from can_be_shipped import CanBeShipped

BASE_SHIPPING_FEE = 5.00   # flat fee per item
RATE_PER_KG = 2.00         # extra cost per kg


class PhysicalProduct(Product, CanBeShipped):
    """A PhysicalProduct IS-A Product (inheritance)
    and CAN-BE-SHIPPED (implements the interface)."""

    def __init__(self, product_id, name, price, stock, weight, history=None):
        super().__init__(product_id, name, price, stock, history)  # reuse Product's constructor
        self.__weight = weight  # in kg

    def get_weight(self):
        return self.__weight

    # Overriding: reuse the parent's output, then add the weight
    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    # Required by the abstract Product class
    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    # Required by the CanBeShipped interface
    def calculate_shipping_cost(self):
        return BASE_SHIPPING_FEE + RATE_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
    