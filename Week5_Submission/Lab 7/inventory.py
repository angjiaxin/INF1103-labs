class Inventory:
    """Responsibility: manage a COLLECTION of Product objects.
    It works with any kind of Product (physical or digital) and calls
    their methods, but never does a product's job for it."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Adds a Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_product(self, product_id):
        """Returns the Product with this exact ID, or None."""
        for product in self.__products:
            if product.get_product_id() == product_id.upper():
                return product
        return None

    def search_product(self, term):
        """Returns a list of Products whose ID or name matches the term."""
        return [p for p in self.__products if p.matches(term)]

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 55)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()  # each product type displays itself
        print("-" * 55)

    def get_products(self):
        return list(self.__products)
    