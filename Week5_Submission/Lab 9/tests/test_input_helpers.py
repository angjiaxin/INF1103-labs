import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import get_positive_float, get_positive_int, get_non_negative_int


def run_with_inputs(function, inputs: list[str]):
    """Runs an input helper with fake typed answers and captures what it prints."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
        result = function("Price: ")
    return result, output.getvalue().splitlines()


class TestInputHelpers(unittest.TestCase):

    def test_get_positive_float_asks_again_until_valid(self):
        result, printed = run_with_inputs(get_positive_float, ["abc", "-5", "12.50"])
        self.assertEqual(result, 12.50)
        self.assertEqual(printed, [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_get_positive_float_rejects_zero(self):
        result, printed = run_with_inputs(get_positive_float, ["0", "3"])
        self.assertEqual(result, 3.0)
        self.assertEqual(len(printed), 1)

    def test_get_positive_int_rejects_text_decimals_and_zero(self):
        result, printed = run_with_inputs(get_positive_int, ["two", "1.5", "0", "2"])
        self.assertEqual(result, 2)
        self.assertEqual(len(printed), 3)

    def test_get_non_negative_int_allows_zero(self):
        result, printed = run_with_inputs(get_non_negative_int, ["-1", "0"])
        self.assertEqual(result, 0)
        self.assertEqual(len(printed), 1)


if __name__ == "__main__":
    unittest.main()
