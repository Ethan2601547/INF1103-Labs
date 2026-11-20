#tests/test_exceptions.py
#Checks the rule "each except catches a specific exception" by reading the project's own code:
#no bare "except:" and no catch-all "except Exception".

import ast
import os
import unittest

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILES = ["main.py", "file_handler.py", "product.py", "physical_product.py", "digital_product.py",
                 "supplier.py", "inventory.py", "order.py", "order_line.py", "product_factory.py",
                 "discount_strategy.py"]

class TestSpecificExceptions(unittest.TestCase):
    def test_no_bare_or_catch_all_except(self) -> None:
        for filename in PROJECT_FILES:
            with open(os.path.join(PROJECT_FOLDER, filename)) as file:
                tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    where = f"{filename}, line {node.lineno}"
                    self.assertIsNotNone(node.type, f"bare except in {where}")
                    if isinstance(node.type, ast.Name):
                        self.assertNotIn(node.type.id, ("Exception", "BaseException"), f"catch-all except in {where}")

if __name__ == "__main__":
    unittest.main()
