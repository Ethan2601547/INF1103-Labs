#tests/test_input.py
#Tests that invalid user input is handled without crashing, and the user is asked again.
#input() is replaced with a fake that hands back a prepared list of answers.

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import get_positive_float

class TestGetPositiveFloat(unittest.TestCase):
    def run_with_answers(self, answers: list[str]) -> tuple[float, str]:
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            value = get_positive_float("Price: ")
        return value, output.getvalue()

    def test_valid_number_is_returned_immediately(self) -> None:
        value, printed = self.run_with_answers(["12.50"])
        self.assertEqual(value, 12.5)
        self.assertEqual(printed, "")

    def test_text_is_rejected_and_user_is_asked_again(self) -> None:
        value, printed = self.run_with_answers(["abc", "12.50"])
        self.assertEqual(value, 12.5)
        self.assertEqual(printed, "Please enter a valid number, e.g. 12.50\n")

    def test_negative_and_zero_are_rejected(self) -> None:
        value, printed = self.run_with_answers(["-5", "0", "3"])
        self.assertEqual(value, 3.0)
        self.assertEqual(printed.count("Please enter a number greater than zero."), 2)

    def test_abc_then_minus_5_then_12_50(self) -> None:
        value, printed = self.run_with_answers(["abc", "-5", "12.50"])
        self.assertEqual(value, 12.5)
        self.assertEqual(printed.splitlines(),
                         ["Please enter a valid number, e.g. 12.50",
                          "Please enter a number greater than zero."])

    def test_empty_input_is_rejected(self) -> None:
        value, _ = self.run_with_answers(["", "7"])
        self.assertEqual(value, 7.0)

if __name__ == "__main__":
    unittest.main()
