#tests/test_factory.py
#Tests for the Factory pattern: products are created through ProductFactory.

import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory

class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier, 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.name, "Lamp")

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, self.supplier, 250.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_factory_returns_the_product_type(self) -> None:
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_fulfillment_info(), "Physical product - needs packing and shipping to customer.")

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_factory_passes_the_supplier_to_the_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, self.supplier)
        self.assertIs(product.supplier, self.supplier)

if __name__ == "__main__":
    unittest.main()
