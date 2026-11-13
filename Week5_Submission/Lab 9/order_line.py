from product import Product


class OrderLine:
    """Responsibility: ONE product and the quantity of it within an order.

    Composition: an OrderLine is created by an Order and belongs to that Order
    only. It is never created elsewhere or moved to another Order.

    Association: the OrderLine refers to a Product, but does not own it.
    """

    def __init__(self, product: Product, quantity: int):
        # Validation: the OrderLine protects its own quantity
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product   # reference only (association)
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_product_id()} | {self.__product.get_name()} | "
              f"Qty: {self.__quantity} x ${self.__product.get_price():.2f} = "
              f"${self.calculate_subtotal():.2f}")
