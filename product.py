#product.py
#responsible for representing and managing a product

from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__supplier: Supplier = supplier

        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price: float = price

        self.__stock: int = 0
        self.update_stock(stock)

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    @abstractmethod
    def get_fulfillment_info(self) -> str:
        """Return a message explaining how this product reaches the customer."""
        pass