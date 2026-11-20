#tests/test_load_products.py
#Tests for load_products(): a missing file is handled gracefully, and bad rows are
#reported and skipped while the valid rows still load.

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from inventory import Inventory
from file_handler import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""

class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "products.csv")

    def write_csv(self, text: str) -> None:
        with open(self.path, "w", newline="") as file:
            file.write(text)

    def load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        self.write_csv(CSV_TEXT)
        self.load(self.path)
        ids = [product.product_id for product in self.inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])

    def test_bad_rows_are_reported(self) -> None:
        self.write_csv(CSV_TEXT)
        lines = self.load(self.path)
        self.assertIn("Row 4 skipped: Unknown product type: service", lines)
        self.assertTrue(any(line.startswith("Row 5 skipped:") for line in lines))

    def test_message_order_and_count(self) -> None:
        self.write_csv(CSV_TEXT)
        lines = self.load(self.path)
        self.assertEqual(lines[-2], "3 products loaded.")
        self.assertEqual(lines[-1], "Load attempt finished.")

    def test_missing_file_does_not_crash(self) -> None:
        missing = os.path.join(self.folder.name, "nothing_here.csv")
        lines = self.load(missing)
        self.assertEqual(lines, [f"Products file not found: {missing}", "Load attempt finished."])
        self.assertEqual(len(self.inventory.get_products()), 0)

    def test_short_row_is_skipped(self) -> None:
        self.write_csv("product_type,product_id,name,price,stock_quantity\nphysical,P001,Lamp\n")
        lines = self.load(self.path)
        self.assertIn("0 products loaded.", lines)

    def test_duplicate_id_is_skipped(self) -> None:
        self.write_csv("h,h,h,h,h\nphysical,P001,Lamp,5.0,1\nphysical,P001,Lamp again,6.0,2\n")
        lines = self.load(self.path)
        self.assertIn("1 products loaded.", lines)

if __name__ == "__main__":
    unittest.main()
