#inventory.py
#responsible for managing a collection of Products
#aggregation: Inventory groups Product objects that already exist. It does not create them
#removing a Product from the Inventory does not destroy the Product

from product import Product                                               #for type hinting

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            return None
        self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def display_all(self) -> None:                                                  #displays all products by asking each product
        print("\nCurrent Inventory:")
        print("-" * 48)
        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def get_products(self) -> list[Product]:
        return list(self.__products)                                        #returns a COPY of the list (used later when saving)