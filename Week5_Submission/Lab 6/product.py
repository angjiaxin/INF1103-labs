TAX_RATE = 0.10


class Product:
    """Responsibility: represent and manage ONE product."""

    def __init__(self, product_id, name, price, stock, history=None):
        self.__product_id = product_id.upper()
        self.__name = name
        self.__price = price
        self.__stock = stock
        # If no history is given (brand new product), start it with the opening stock
        if history is None:
            self.__history = [stock]
        else:
            self.__history = history

    # ---------- Getters (read-only access from outside) ----------
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_history(self):
        return list(self.__history)  # return a copy so outside code can't change it

    # ---------- Behaviour ----------
    def update_stock(self, quantity):
        """Adds a delivery to stock. The Product decides what is allowed."""
        if quantity < 0:
            raise ValueError("Delivery quantity cannot be negative.")
        self.__stock += quantity
        self.__history.append(quantity)

    def calculate_tax(self, amount):
        return amount * TAX_RATE

    def is_overstocked(self, limit):
        return self.__stock > limit

    def matches(self, term):
        """True if term equals the ID or appears in the name (case-insensitive)."""
        term = term.lower()
        return term == self.__product_id.lower() or term in self.__name.lower()

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Converts the product to a dictionary so it can be saved as JSON."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "history": self.__history
        }