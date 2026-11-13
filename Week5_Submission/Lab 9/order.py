from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount


class Order:
    """Responsibility: manage ONE customer order.

    Composition: the Order creates its own OrderLine objects inside
    add_order_line(). OrderLines are never passed in from outside, and when
    a line is removed (or the Order goes away) the OrderLine goes with it.

    Strategy pattern (association): the Order is GIVEN a DiscountStrategy and
    only calls its apply() method. It contains no if/elif about discount types,
    and the same strategy object can be shared by many orders.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id.upper()
        self.__order_lines: list[OrderLine] = []
        if discount is None:
            discount = NoDiscount()
        self.__discount: DiscountStrategy = discount

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the strategy later without changing anything else."""
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Takes a Product and quantity, and CREATES the OrderLine internally.
        The OrderLine itself validates the quantity."""
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

    def calculate_subtotal(self) -> float:
        """Total BEFORE discount: asks each OrderLine for its own subtotal."""
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    def calculate_total(self) -> float:
        """Total AFTER discount: the strategy decides how to discount."""
        return self.__discount.apply(self.calculate_subtotal())

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 55)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 55)
        subtotal = self.calculate_subtotal()
        total = self.calculate_total()
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount ({type(self.__discount).__name__}): -${subtotal - total:.2f}")
        print(f"Order Total: ${total:.2f}")
