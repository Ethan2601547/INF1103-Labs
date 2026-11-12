#responsible for representing a virtual product that has size (megabytes)

from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def get_fulfillment_info(self) -> str:
        return "Digital product - can be downloaded directly by the customer. No shipping required."