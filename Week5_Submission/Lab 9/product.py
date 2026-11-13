from abc import ABC, abstractmethod

from supplier import Supplier

TAX_RATE: float = 0.10


class Product(ABC):
    """Responsibility: represent and manage ONE product.

    Abstract class: every product must be either physical or digital,
    so a plain Product can never be created directly.

    Association: a Product keeps a reference to the Supplier that supplies it,
    but it does not own the Supplier. Both can exist independently.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, history: list[int] | None = None):
        # Validation: Product owns these rules, so every subclass inherits them (LSP)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__product_id: str = product_id.upper()
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier   # reference only (association)
        # If no history is given (brand new product), start it with the opening stock
        if history is None:
            self.__history: list[int] = [stock]
        else:
            self.__history = history

    # ---------- Abstract method (each child MUST implement this) ----------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    # ---------- Getters (read-only access from outside) ----------
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_history(self) -> list[int]:
        return list(self.__history)  # return a copy so outside code can't change it

    # ---------- Behaviour ----------
    def update_stock(self, quantity: int) -> None:
        """Adds a delivery to stock. Every subclass keeps this same meaning (LSP)."""
        if quantity < 0:
            raise ValueError("Delivery quantity cannot be negative.")
        self.__stock += quantity
        self.__history.append(quantity)

    def calculate_tax(self, amount: int) -> float:
        return amount * TAX_RATE

    def is_overstocked(self, limit: int) -> bool:
        return self.__stock > limit

    def matches(self, term: str) -> bool:
        """True if term equals the ID or appears in the name (case-insensitive)."""
        term = term.lower()
        return term == self.__product_id.lower() or term in self.__name.lower()

    def display_information(self) -> None:
        """Common information. Child classes add their own details after this."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
              f"Supplier: {self.__supplier.get_name()}")

    def to_dict(self) -> dict:
        """Common data for saving. Child classes add their type and extra fields."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "history": self.__history,
            "supplier": self.__supplier.to_dict()
        }
