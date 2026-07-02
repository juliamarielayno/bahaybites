"""
BahayBites database helper.

Usage in your Streamlit app:
    from db import init_db, get_connection, record_order, get_pack_sizes, weekly_summary

    init_db()  # run once, safe to call every startup (CREATE TABLE IF NOT EXISTS)
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date

DB_PATH = Path(__file__).parent / "bahaybites.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't exist, then seed current menu if empty."""
    conn = get_connection()
    schema_path = Path(__file__).parent / "schema.sql"
    conn.executescript(schema_path.read_text())
    conn.commit()

    if conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
        _seed_menu(conn)
    conn.close()


def _seed_menu(conn):
    """Seed items, pack sizes, and ingredient prices from your current menu."""
    items = [
        ("Pandesal", "Regular Menu"),
        ("Ensaymada", "Regular Menu"),
        ("Spanish Bread", "Regular Menu"),
        ("Ube Crinkle Cookies", "Weekly Drop"),
        ("Bahay Basket", "Bahay Basket"),
    ]
    conn.executemany("INSERT INTO items (name, category) VALUES (?, ?)", items)

    item_ids = {row["name"]: row["item_id"] for row in conn.execute("SELECT item_id, name FROM items")}

    pack_sizes = [
        (item_ids["Pandesal"], "Half Dozen", 6, 6.00),
        (item_ids["Pandesal"], "Dozen", 12, 10.00),
        (item_ids["Ensaymada"], "Four", 4, 12.00),
        (item_ids["Ensaymada"], "Half Dozen", 6, 15.00),
        (item_ids["Spanish Bread"], "Four", 4, 10.00),
        (item_ids["Spanish Bread"], "Half Dozen", 6, 12.00),
        (item_ids["Ube Crinkle Cookies"], "Single", 1, 3.00),
        (item_ids["Ube Crinkle Cookies"], "Four", 4, 10.00),
        (item_ids["Ube Crinkle Cookies"], "Half Dozen", 6, 12.00),
        (item_ids["Bahay Basket"], "Basket", 1, 20.00),
    ]
    conn.executemany(
        "INSERT INTO pack_sizes (item_id, label, units_per_pack, price) VALUES (?, ?, ?, ?)",
        pack_sizes,
    )

    ingredient_prices = [
        ("bread_flour", "oz", 0.03),
        ("sugar", "oz", 0.0375),
        ("yeast", "oz", 0.31),
        ("instant_mash", "oz", 0.17),
        ("oil", "fl_oz", 0.073),
        ("salt", "oz", 0.032),
        ("butter", "oz", 0.279),
        ("egg", "egg", 0.137),
        ("milk", "fl_oz", 0.022),
        ("cornstarch", "oz", 0.013),
        ("ube_jam", "oz", 0.90),
        ("ube_extract", "oz", 0.845),
        ("vanilla_extract", "oz", 1.31),
        ("confectioners", "oz", 0.062),
        ("baking_powder", "oz", 0.262),
    ]
    conn.executemany(
        "INSERT INTO ingredient_prices (ingredient_name, unit, unit_cost) VALUES (?, ?, ?)",
        ingredient_prices,
    )
    conn.commit()


def get_pack_sizes(conn=None):
    """Return all active pack sizes joined with item name — use this to build
    your Streamlit input widgets instead of hardcoding them."""
    close = conn is None
    conn = conn or get_connection()
    rows = conn.execute("""
        SELECT ps.pack_size_id, i.name AS item_name, ps.label, ps.units_per_pack, ps.price
        FROM pack_sizes ps JOIN items i ON ps.item_id = i.item_id
        WHERE ps.active = 1
        ORDER BY i.name, ps.units_per_pack
    """).fetchall()
    if close:
        conn.close()
    return rows


def record_order(week_start: str, pickup_date: str, line_items: list, customer_name: str = None):
    """
    line_items: list of dicts like {"pack_size_id": 3, "quantity": 2}
    week_start / pickup_date: 'YYYY-MM-DD' strings
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (week_start, pickup_date, customer_name) VALUES (?, ?, ?)",
        (week_start, pickup_date, customer_name),
    )
    order_id = cur.lastrowid

    for li in line_items:
        pack = conn.execute(
            "SELECT price FROM pack_sizes WHERE pack_size_id = ?", (li["pack_size_id"],)
        ).fetchone()
        unit_price = pack["price"]
        revenue = unit_price * li["quantity"]
        cur.execute(
            """INSERT INTO order_line_items (order_id, pack_size_id, quantity, unit_price, line_revenue)
               VALUES (?, ?, ?, ?, ?)""",
            (order_id, li["pack_size_id"], li["quantity"], unit_price, revenue),
        )
    conn.commit()
    conn.close()
    return order_id


def weekly_summary():
    """Revenue and units per item per week — the exact table a forecasting
    model will train on later."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT o.week_start,
               i.name AS item_name,
               ps.label AS pack_label,
               SUM(oli.quantity) AS packs_sold,
               SUM(oli.quantity * ps.units_per_pack) AS units_sold,
               SUM(oli.line_revenue) AS revenue
        FROM order_line_items oli
        JOIN orders o ON oli.order_id = o.order_id
        JOIN pack_sizes ps ON oli.pack_size_id = ps.pack_size_id
        JOIN items i ON ps.item_id = i.item_id
        GROUP BY o.week_start, i.name, ps.label
        ORDER BY o.week_start, i.name
    """).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
    print("\nSeeded pack sizes:")
    for row in get_pack_sizes():
        print(f"  {row['item_name']} — {row['label']}: {row['units_per_pack']} units @ ${row['price']:.2f}")
