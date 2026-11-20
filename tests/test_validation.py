#tests/test_validation.py
#Tests that invalid prices, stock quantities and order quantities are rejected.
#Each rule is enforced by the class that owns it, so a subclass cannot skip it (LSP).

import unittest

from supplier import Supplier
from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order_line import OrderLine

class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier)

    def test_price_of_zero_is_rejected(self) -> None:
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P002", "Free", 0, 10, self.supplier, 1.0)
        self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_negative_price_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P002", "Bad", -5.0, 10, self.supplier, 1.0)

    def test_negative_stock_is_rejected_when_creating(self) -> None:
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P002", "Bad", 5.0, -1, self.supplier, 1.0)
        self.assertEqual(str(context.exception), "Stock cannot be negative.")

    def test_negative_stock_is_rejected_when_updating(self) -> None:
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)
        self.assertEqual(self.product.stock, 10)                #the bad update did not change anything

    def test_zero_stock_is_allowed(self) -> None:
        self.product.update_stock(0)
        self.assertEqual(self.product.stock, 0)

    def test_digital_product_follows_the_same_rules_as_product(self) -> None:
        with self.assertRaises(ValueError):
            DigitalProduct("D001", "Bad", 0, 10, self.supplier, 5.0)
        with self.assertRaises(ValueError):
            DigitalProduct("D001", "Bad", 5.0, -1, self.supplier, 5.0)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.product, -3)

    def test_valid_order_line_is_accepted(self) -> None:
        self.assertEqual(OrderLine(self.product, 2).quantity, 2)

if __name__ == "__main__":
    unittest.main()
