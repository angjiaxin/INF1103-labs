from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A DigitalProduct IS-A Product. It does NOT implement CanBeShipped,
    because digital products are downloaded, not shipped.

    LSP: it keeps update_stock() exactly as Product defines it.
    For a digital product, stock means the number of licences available."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float,
                 history: list[int] | None = None):
        # pass the Supplier up to Product using super()
        super().__init__(product_id, name, price, stock, supplier, history)
        self.__download_size: float = download_size  # in MB

    def get_download_size(self) -> float:
        return self.__download_size

    # Overriding: reuse the parent's output, then add the download size
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    # Required by the abstract Product class
    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data