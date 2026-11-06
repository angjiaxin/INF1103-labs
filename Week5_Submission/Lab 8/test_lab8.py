from product import Product


class DigitalProduct(Product):
    """A DigitalProduct IS-A Product. It does NOT implement CanBeShipped,
    because digital products are downloaded, not shipped."""

    def __init__(self, product_id, name, price, stock, download_size, history=None):
        super().__init__(product_id, name, price, stock, history)  # reuse Product's constructor
        self.__download_size = download_size  # in MB

    def get_download_size(self):
        return self.__download_size

    # Overriding: reuse the parent's output, then add the download size
    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    # Required by the abstract Product class
    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data