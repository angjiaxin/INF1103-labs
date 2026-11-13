import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from inventory import Inventory
from product_loader import load_products
from tests.helpers import make_supplier

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        # Write the lab's CSV into a temporary folder, so the test never
        # depends on (or changes) the real products.csv
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")
        with open(self.path, "w", newline="") as f:
            f.write(LAB_CSV)

    def tearDown(self):
        self.folder.cleanup()

    def load(self, path: str) -> tuple[Inventory, list[str]]:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, inventory, make_supplier())
        return inventory, output.getvalue().splitlines()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        inventory, printed = self.load(self.path)
        loaded_ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", printed[0])
        self.assertIn("could not convert string to float: 'abc'", printed[1])
        self.assertEqual(printed[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_gracefully(self):
        missing = os.path.join(self.folder.name, "renamed.csv")
        inventory, printed = self.load(missing)
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(printed, [f"Products file not found: {missing}",
                                   "Load attempt finished."])

    def test_loading_twice_skips_duplicate_ids(self):
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(self.path, inventory, make_supplier())
            load_products(self.path, inventory, make_supplier())   # same file again
        self.assertEqual(len(inventory.get_products()), 3)
        self.assertIn("0 products loaded.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
