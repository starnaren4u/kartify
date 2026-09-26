import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kartify.tools import OrderDetails


class FetchOrderDetailsTests(unittest.TestCase):
    def test_returns_matching_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "kartify.db"
            with sqlite3.connect(database_path) as connection:
                connection.execute(
                    "CREATE TABLE orders (order_id TEXT, status TEXT)"
                )
                connection.execute(
                    "INSERT INTO orders (order_id, status) VALUES (?, ?)",
                    ("O40327", "shipped"),
                )

            with patch.object(OrderDetails, "DATABASE_PATH", database_path):
                result = OrderDetails.fetch_order_details.invoke(
                    {"order_id": "O40327"}
                )

        self.assertIn("O40327", result)
        self.assertIn("shipped", result)


if __name__ == "__main__":
    unittest.main()
