
import re
import sqlite3
from pathlib import Path

import pandas as pd
from langchain_core.tools import tool


DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "kartify.db"

@tool
def fetch_order_details(order_id: str) -> str:
    """
    Fetch all order details for a given order_id from the Kartify database.
    Use this tool whenever the customer's query requires order-specific information.
    Returns a formatted string of order details, or an error message if not found.
    """
    # Validate order_id format (must match pattern like O12345)
    if not re.match(r'^O\d+$', order_id.strip()):
        return f"Invalid order ID format: '{order_id}'. Expected format: O followed by digits (e.g. O40327)."
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            df = pd.read_sql_query(
                "SELECT * FROM orders WHERE order_id = ?",
                conn,
                params=(order_id.strip(),)
            )
        if df.empty:
            return f"No order found with ID {order_id}."
        return df.to_string(index=False)
    except Exception as e:
        return f"Database error while fetching order {order_id}: {str(e)}"
