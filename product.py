#product.py
#responsible for representing and managing a product

class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name

        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price
        
        self.__stock = 0
        self.update_stock(stock)

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")