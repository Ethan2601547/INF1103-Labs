#responsible for representing 1 product and its quantity inside an order
#OrderLine refers to a Product, but it does not own that Product
#Do not create an OrderLine elsewhere and pass it into the Order

from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a whole number greater than 0.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"    {self.__product.name} x {self.__quantity} @ ${self.__product.price:.2f} "f"= ${self.calculate_subtotal():.2f}")