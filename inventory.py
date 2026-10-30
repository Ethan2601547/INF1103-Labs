#inventory.py
#responsible for managing a collection of Products

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.product_id)  is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def display_all(self):                                                  #displays all products by asking each product
        print("\nCurrent Inventory:")
        print("-" * 48)
        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def get_products(self):
        return list(self.__products)                                        #returns a COPY of the list (used later when saving)