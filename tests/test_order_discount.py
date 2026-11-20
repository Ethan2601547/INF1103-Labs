#tests/test_order_discount.py
#Tests that Order calculates totals through a DiscountStrategy.

import ast
import inspect
import textwrap
import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount

def make_order_worth_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S001", "Test Supplier", "test@example.com")
    product = PhysicalProduct("P001", "Widget", 50.0, 100, supplier, 1.0)
    order = Order("O001", discount)
    order.add_order_line(product, 5)                                              #5 x 50.00 = 250.00
    return order

class TestOrderDiscount(unittest.TestCase):
    def test_default_order_uses_no_discount(self) -> None:
        self.assertEqual(make_order_worth_250().calculate_total(), 250.0)

    def test_order_total_goes_through_the_strategy(self) -> None:
        order = make_order_worth_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)

    def test_strategy_can_be_changed_with_set_discount(self) -> None:
        order = make_order_worth_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)
        order.set_discount(NoDiscount())
        self.assertEqual(order.calculate_total(), 250.0)

    def test_a_brand_new_strategy_defined_in_the_test_also_works(self) -> None:
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2
        order = make_order_worth_250(HalfPrice())
        self.assertEqual(order.calculate_total(), 125.0)

    def test_calculate_total_contains_no_discount_if_elif_logic(self) -> None:
        #parse the real code of calculate_total() and look for any if/elif statement in it
        source = textwrap.dedent(inspect.getsource(Order.calculate_total))
        if_statements = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.If)]
        self.assertEqual(if_statements, [])

if __name__ == "__main__":
    unittest.main()
