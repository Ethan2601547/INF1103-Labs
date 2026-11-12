#responsible for representing a physical product that has weight

from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    # Simple shipping rule: a flat fee plus charge for every kilo
    SHIPPING_BASE_FEE = 5.00
    SHIPPING_FEE_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)

        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        shipping = self.calculate_shipping_cost()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg | Shipping: ${shipping:.2f}")

    def get_fulfillment_info(self) -> str:
        return "Physical product - needs packing and shipping to customer."

    def calculate_shipping_cost(self) -> float:
        return self.SHIPPING_BASE_FEE + (self.SHIPPING_FEE_PER_KG * self.__weight)