"""
report.py - sales summary & time-of-day chart

Flags:
  -c / --category CAT [CAT …]   {one or more product categories}
  -m / --metric {revenue,units} {£ or units}
  -g / --group-by {item,category}{bar colours}

One bar per 30-min slot (07 : 30  -> 23 : 00). Days are collapsed, so x-axis is a tidy categorical timeline.
"""
from __future__ import annotations

import argparse
import sqlite3
from contextlib import closing
import sys, textwrap

import pandas as pd
import plotly.express as px
import plotly.io as pio

DB_PATH = "pos.db"
pio.renderers.default = "browser"

# CLI

def get_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--category", nargs="+", help="{category filter - space-separated}")
    ap.add_argument("-m", "--metric", choices=["revenue", "units"], default="revenue", help="{£ or units}")
    ap.add_argument("-g", "--group-by", choices=["item", "category"], default="item", dest="group_by", help="{colour by}")
    return ap.parse_args()

# SQL WHERE

def where_clause(cats: list[str] | None) -> tuple[str, list]:
    if cats:
        qs = ",".join("?" for _ in cats)
        return f"WHERE c.cat IN ({qs})", cats
    return "", []

# console summary

def show_summary(cur: sqlite3.Cursor, where: str, params: list, metric: str, group: str) -> None:
    cur.execute(f"SELECT COUNT(*) n FROM orders o JOIN consumables c ON c.id = o.cons_id {where}", params)
    print("Total order lines:", cur.fetchone()["n"])

    metric_col = "revenue" if metric == "revenue" else "units"
    label_col = "c.name" if group == "item" else "c.cat"
    hdr = "Product" if group == "item" else "Category"

    cur.execute(textwrap.dedent(f"""
        SELECT {label_col} label,
               SUM(o.qty) units,
               ROUND(SUM(o.qty*c.sale_price),2) revenue
        FROM orders o JOIN consumables c ON c.id = o.cons_id
        {where}
        GROUP BY label
        ORDER BY {metric_col} DESC
        LIMIT 10
    """), params)

    print(f"\nTop {group}s by {metric}")
    print(f"{hdr:<25}{'Units':>7}{'Revenue':>11}")
    for r in cur.fetchall():
        print(f"{r['label']:<25}{r['units']:>7}£{r['revenue']:>10}")

# load raw data

def load_df(cats: list[str] | None) -> pd.DataFrame:
    where, params = where_clause(cats)
    with closing(sqlite3.connect(DB_PATH)) as con:
        return pd.read_sql_query(textwrap.dedent(f"""
            SELECT t.day, t.time,
                   c.name item, c.cat category,
                   o.qty, c.sale_price,
                   o.qty*c.sale_price line_total
            FROM orders o
            JOIN time_rec t ON t.id = o.time_id
            JOIN consumables c ON c.id = o.cons_id
            {where}
            ORDER BY t.day, t.time
        """), con, params=params)

# aggregate to 30-min slots

def slot_df(df: pd.DataFrame, metric: str, group: str) -> pd.DataFrame:
    df["slot"] = pd.to_datetime(df["day"] + " " + df["time"]).dt.floor("30min")
    df["time"] = df["slot"].dt.strftime("%H:%M")  # e.g. 13:30

    val = "revenue" if metric == "revenue" else "units"
    df[val] = df["line_total"] if metric == "revenue" else df["qty"]
    label = "item" if group == "item" else "category"

    return (df.groupby(["time", label], as_index=False)
              .agg(**{val: (val, "sum")})
              .rename(columns={label: "label"}))

# draw chart

def make_chart(df: pd.DataFrame, metric: str, group: str, cats: list[str] | None) -> None:
    val = "revenue" if metric == "revenue" else "units"
    ylab = "£ Revenue" if metric == "revenue" else "Units Sold"

    title = f"{ylab.split()[0]} by 30-min slot"
    if group == "category":
        title += " (categories)"
    if cats:
        title += " [" + ", ".join(cats) + "]"

    # slots 07:30  -> 23:00
    cat_order = [f"{h:02d}:{m:02d}" for h in range(7, 23) for m in (30, 0)] + ["23:00"]
    cat_order = cat_order[1:]  # start at 07:30

    fig = px.bar(df, x="time", y=val, color="label", title=title,
                 category_orders={"time": cat_order},
                 labels={"time": "Time of Day", val: ylab, "label": group})

    fig.update_xaxes(type="category")
    fig.update_traces(marker_line_width=0, width=0.9)
    fig.write_html("output.html", include_plotlyjs="cdn", full_html=True)
    print("Chart saved to output.html")

# main

def main() -> None:
    args = get_args()
    where, params = where_clause(args.category)
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.row_factory = sqlite3.Row
        show_summary(con.cursor(), where, params, args.metric, args.group_by)
    df = load_df(args.category)
    if df.empty:
        sys.exit("No data.")
    make_chart(slot_df(df, args.metric, args.group_by), args.metric, args.group_by, args.category)

if __name__ == "__main__":
    main()