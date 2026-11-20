#tests/test_discounts.py
#Automated tests for the Strategy pattern. Run from the project folder with:
#    python -m unittest discover -s tests -t . -v

import unittest

from discount_strategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount_takes_percentage_off(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_applies_at_or_above_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertEqual(BulkDiscount(200, 20).apply(200.0), 180.0)      #exactly on the threshold counts

    def test_bulk_discount_ignored_below_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_bulk_discount_never_goes_negative(self) -> None:
        self.assertEqual(BulkDiscount(0, 50).apply(10.0), 0.0)

    def test_student_discount_takes_5_percent_off(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(200.0), 190.0)

    def test_invalid_strategy_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(-5)
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)

    def test_strategy_base_class_cannot_be_created(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()                          # type: ignore[abstract]

if __name__ == "__main__":
    unittest.main()
