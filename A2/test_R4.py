import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import R4


class TestR4Dashboard(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {
                "order_number": [1, 2, 3],
                "employee_id": [100, 100, 200],
                "employee_name": ["A", "A", "B"],
                "sales_region": ["West", "West", "East"],
                "order_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "order_type": ["Retail", "Wholesale", "Retail"],
                "customer_type": ["Individual", "Business", "Individual"],
                "customer_state": ["HI", "HI", "CA"],
                "product_category": ["Oil", "Oil", "Soap"],
                "quantity": [1, 2, 3],
                "unit_price": [10.0, 20.0, 5.0],
                "sales": [10.0, 40.0, 15.0],
            }
        )

    def test_validate_required_fields_present(self):
        output = io.StringIO()
        with redirect_stdout(output):
            R4.validate_required_fields(self.data)
        self.assertIn("All required fields", output.getvalue())

    def test_validate_required_fields_missing(self):
        output = io.StringIO()
        with redirect_stdout(output):
            R4.validate_required_fields(self.data.drop(columns=["order_type"]))
        self.assertIn("missing required field", output.getvalue().lower())

    def test_require_columns(self):
        self.assertTrue(R4.require_columns(self.data, {"sales_region"}, "test"))
        self.assertFalse(R4.require_columns(self.data, {"does_not_exist"}, "test"))

    def test_load_csv_success(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as file:
            temp_path = Path(file.name)
        try:
            self.data.drop(columns=["sales"]).to_csv(temp_path, index=False)
            loaded = R4.load_csv(temp_path)
            self.assertIsInstance(loaded, pd.DataFrame)
            self.assertIn("sales", loaded.columns)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_load_csv_failure(self):
        with self.assertRaises(SystemExit):
            R4.load_csv("not_a_real_file.csv")

    def test_display_initial_rows_skip(self):
        with patch("builtins.input", side_effect=[""]):
            result = R4.display_initial_rows(self.data)
        self.assertIsNone(result)

    def test_display_initial_rows_valid_count(self):
        with patch("builtins.input", side_effect=["2"]):
            result = R4.display_initial_rows(self.data)
        self.assertEqual(len(result), 2)

    def test_display_initial_rows_invalid_then_valid(self):
        with patch("builtins.input", side_effect=["0", "all"]):
            result = R4.display_initial_rows(self.data)
        self.assertEqual(len(result), len(self.data))

    def test_predefined_analytics_return_pivots(self):
        self.assertIsInstance(R4.sales_by_region_order_type(self.data), pd.DataFrame)
        self.assertIsInstance(R4.average_sales_by_region_with_state_sale_type(self.data), pd.DataFrame)
        self.assertIsInstance(R4.sales_by_customer_type_order_type_by_state(self.data), pd.DataFrame)
        self.assertIsInstance(R4.total_sales_quantity_and_price_by_region_and_product(self.data), pd.DataFrame)
        self.assertIsInstance(R4.total_sales_quantity_and_price_by_customer_type(self.data), pd.DataFrame)
        self.assertIsInstance(R4.max_min_sales_price_by_category(self.data), pd.DataFrame)
        self.assertIsInstance(R4.unique_employees_by_region(self.data), pd.DataFrame)

    def test_get_user_selection_recovery(self):
        with patch("builtins.input", side_effect=["99", "1,2"]):
            result = R4.get_user_selection(["a", "b", "c"], "Select:")
        self.assertEqual(result, ["a", "b"])

    def test_get_user_selection_optional_empty(self):
        with patch("builtins.input", side_effect=[""]):
            result = R4.get_user_selection(["a", "b"], "Select:", allow_empty=True)
        self.assertEqual(result, [])

    def test_generate_custom_pivot_table(self):
        # rows=sales_region, columns=none, values=first numeric option, aggfunc=sum
        with patch("builtins.input", side_effect=["4", "", "1", "1"]):
            pivot = R4.generate_custom_pivot_table(self.data)
        self.assertIsInstance(pivot, pd.DataFrame)

    def test_display_menu_recovery(self):
        with patch("builtins.input", side_effect=["bad", "10"]):
            choice, menu_options = R4.display_menu()
        self.assertEqual(choice, 10)
        self.assertEqual(len(menu_options), 10)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            R4.exit_program(self.data)


if __name__ == "__main__":
    unittest.main()
