#responsible for representing a physical product that has weight

from product import Product

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")