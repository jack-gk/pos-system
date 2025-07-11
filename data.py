import sqlite3

DB_PATH = "pos.db"

def get_conn():
    # isolation_level=None → autocommit, handy for read-only scripts
    return sqlite3.connect(DB_PATH, isolation_level=None)

with get_conn() as con:
    con.row_factory = sqlite3.Row          # rows behave like dicts
    cur = con.cursor()

    # Total sales count
    cur.execute("SELECT COUNT(*) AS n_orders FROM orders")
    print("Orders so far:", cur.fetchone()["n_orders"])

    # Top-selling items
    cur.execute("""
        SELECT item_name,
               SUM(qty) AS units,
               ROUND(SUM(qty * price), 2) AS revenue
        FROM order_lines
        GROUP BY item_id, item_name
        ORDER BY revenue DESC
        LIMIT 10
    """)
    for row in cur.fetchall():
        print(f"{row['item_name']:<25}  {row['units']:>4}  £{row['revenue']}")

import pandas as pd, sqlite3

with sqlite3.connect("pos.db") as con:
    # Orders joined with individual lines—good for timeseries charts
    df = pd.read_sql_query("""
        SELECT o.timestamp,
               l.item_name,
               l.qty,
               l.price,
               l.qty * l.price AS line_total
        FROM order_lines l
        JOIN orders o ON o.id = l.order_id
        ORDER BY o.timestamp
    """, con, parse_dates=["timestamp"])

print(df.head())
# Example: daily revenue
daily = df.groupby(df["timestamp"].dt.date)["line_total"].sum()

print(daily.head())
