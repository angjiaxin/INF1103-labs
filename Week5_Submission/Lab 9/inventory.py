from product import Product


class Inventory:
    """Responsibility: manage a COLLECTION of Product objects.

    Aggregation: the Inventory holds references to Products, but it does not
    create them or control their lifecycle. A Product can exist before it is
    added, and still exists after it is removed or transferred.

    The collection is typed with the base class Product, so it can hold
    PhysicalProduct, DigitalProduct, or any future subclass (LSP).
    """

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Adds an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Removes the Product reference from this inventory and returns it.
        The Product object itself is NOT destroyed."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Returns the Product with this exact ID, or None."""
        for product in self.__products:
            if product.get_product_id() == product_id.upper():
                return product
        return None

    def search_product(self, term: str) -> list[Product]:
        """Returns a list of Products whose ID or name matches the term."""
        return [p for p in self.__products if p.matches(term)]

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 70)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()  # polymorphism: each product displays itself
        print("-" * 70)

    def get_products(self) -> list[Product]:
        return list(self.__products)
