from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    """Factory pattern: the ONE place that decides which Product class to create.

    The rest of the program asks the factory for a Product and only works with
    the Product type, so it does not need to know about PhysicalProduct or
    DigitalProduct.

    A new product type still means adding a branch here (the OCP issue moves
    into the factory). That is acceptable for a small application like this.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, weight: float = 0.0,
               download_size: float = 0.0, history: list[int] | None = None) -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight, history)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, download_size, history)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
