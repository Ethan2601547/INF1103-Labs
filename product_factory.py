#FACTORY: this decides which Product class to create.
#The program asks the factory for a Product and never needs to know about
#PhysicalProduct or DigitalProduct. The factory does not store the products it makes.

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, size: float = 0.0) -> Product:

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, size)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")