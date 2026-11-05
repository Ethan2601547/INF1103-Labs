#responsible for representing a virtual product that has size (megabytes)

from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")