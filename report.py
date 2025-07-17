# report.py  –  simple sales summary + time-of-day bar chart

import sqlite3
from contextlib import closing
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.io as pio

DB_PATH = "pos.db"
pio.renderers.default = "browser"


# 1) Quick console summary

with closing(sqlite3.connect(DB_PATH)) as con:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) AS n_orders FROM orders")
    print("Total order lines:", cur.fetchone()["n_orders"])

    # top-selling products
    cur.execute("""
        SELECT c.name AS item_name,
               SUM(o.qty)                       AS units,
               ROUND(SUM(o.qty * c.sale_price), 2) AS revenue
        FROM orders       o
        JOIN consumables  c ON c.id = o.cons_id
        GROUP BY c.id
        ORDER BY revenue DESC
        LIMIT 10
    """)
    print("\nTop products")
    for row in cur.fetchall():
        print(f"{row['item_name']:<25}  {row['units']:>4}  £{row['revenue']:>6}")


# 2) Pull line-item detail into pandas

with closing(sqlite3.connect(DB_PATH)) as con:
    df = pd.read_sql_query("""
        SELECT t.day,
               t.time,
               c.name           AS item_name,
               o.qty,
               c.sale_price,
               o.qty * c.sale_price AS line_total
        FROM orders       o
        JOIN time_rec     t ON t.id = o.time_id
        JOIN consumables  c ON c.id = o.cons_id
        ORDER BY t.day, t.time
    """, con)


# 3) Build “time_of_day” for 24-hour plots


df["timestamp"] = pd.to_datetime(df["day"] + " " + df["time"])
df["time_of_day"] = df["timestamp"].dt.floor("30min").apply(
    lambda dt: dt.replace(year=1970, month=1, day=1)
)

df_slot = (df.groupby(["time_of_day", "item_name"], as_index=False)
             .agg(revenue=("line_total", "sum")))

print(df_slot.head())


# 4) Bar chart: revenue by 30-min slot, coloured by product


slot_ms = 30 * 60 * 1000

fig = px.bar(
    df_slot,
    x="time_of_day",
    y="revenue",
    color="item_name",
    title="Revenue by 30-min Slot",
    labels={"time_of_day": "Time of Day", "revenue": "£ Revenue"}
)

fig.update_traces(width=0.9 * slot_ms)
fig.update_xaxes(
    tickformat="%H:%M",
    dtick=slot_ms,
    range=[datetime(1970, 1, 1, 7, 30), datetime(1970, 1, 1, 23)]
)
fig.write_html("output.html", include_plotlyjs="cdn", full_html=True)