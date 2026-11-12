#responsible for reprensenting a customer order made up of order lines
#Order creates and manages its own OrderLine objects

from order_line import OrderLine
from product import Product

class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.product.product_id == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)                                      #returns a COPY of the list, so that the original list cannot be modified outside of this class

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if len(self.__order_lines) == 0:
            print("    (No order lines in this order)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"    Total: ${self.calculate_total():.2f}")