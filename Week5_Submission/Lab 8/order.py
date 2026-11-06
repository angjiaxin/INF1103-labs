from product import Product
from order_line import OrderLine


class Order:
    """Responsibility: manage ONE customer order.

    Composition: the Order creates its own OrderLine objects inside
    add_order_line(). OrderLines are never passed in from outside, and when
    a line is removed (or the Order goes away) the OrderLine goes with it.
    """

    def __init__(self, order_id: str):
        self.__order_id: str = order_id.upper()
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Takes a Product and quantity, and CREATES the OrderLine internally."""
        if quantity <= 0:
            raise ValueError("Order quantity must be at least 1.")
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Removes the line for this product. The OrderLine is discarded with it,
        but the Product itself still exists."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)  # copy, so lines can't be added from outside

    def calculate_total(self) -> float:
        """Asks each OrderLine for its own subtotal."""
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 55)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 55)
        print(f"Order Total: ${self.calculate_total():.2f}")