from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped

BASE_SHIPPING_FEE: float = 5.00   # flat fee per item
RATE_PER_KG: float = 2.00         # extra cost per kg


class PhysicalProduct(Product, CanBeShipped):
    """A PhysicalProduct IS-A Product (inheritance)
    and CAN-BE-SHIPPED (implements the interface)."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float, history: list[int] | None = None):
        # pass the Supplier up to Product using super()
        super().__init__(product_id, name, price, stock, supplier, history)
        self.__weight: float = weight  # in kg

    def get_weight(self) -> float:
        return self.__weight

    # Overriding: reuse the parent's output, then add the weight
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    # Required by the abstract Product class
    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    # Required by the CanBeShipped interface
    def calculate_shipping_cost(self) -> float:
        return BASE_SHIPPING_FEE + RATE_PER_KG * self.__weight

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data