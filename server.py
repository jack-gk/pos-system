import sqlite3, os
from datetime import datetime, timezone, timedelta
from contextlib import closing
from flask import Flask, request, jsonify
from flask_cors import CORS
from zoneinfo import ZoneInfo

DB_FILE = "pos.db"

# 1.  Helpers

LONDON = ZoneInfo("Europe/London")

def parse_and_round(ts_raw):
    """Return (day, hh:mm) rounded down to the previous 30-minute slot."""

    match ts_raw:
        case int() | float():
            ts_sec = ts_raw / 1000 if ts_raw > 4e12 else ts_raw
            dt     = datetime.fromtimestamp(ts_sec, tz=timezone.utc)
        case str():
            # fromisoformat handles offsets like +01:00; replace trailing Z → +00:00
            iso = ts_raw.replace("Z", "+00:00")
            dt  = datetime.fromisoformat(iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        case _:
            raise TypeError("timestamp must be ISO-8601 str or epoch number")

    # convert to GMT
    dt_local = dt.astimezone(LONDON)

    # floor to previous 30 minute step
    floored = dt_local.replace(
        minute = (dt_local.minute // 30) * 30,
        second = 0, microsecond = 0
    )

    # return strings seperated
    return floored.strftime("%Y-%m-%d"), floored.strftime("%H:%M")


def get_db_conn():
    con = sqlite3.connect(DB_FILE)
    con.execute("PRAGMA foreign_keys = ON")   # enforce FK constraints
    return con

# 2.  DB bootstrap

def init_db():
    with closing(sqlite3.connect(DB_FILE)) as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS time_rec (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                day   TEXT NOT NULL,
                time  TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS consumables (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT  NOT NULL,
                fb_type     TEXT  NOT NULL CHECK (fb_type IN ('F','B')),
                cat         TEXT  NOT NULL,
                unit_price  REAL  NOT NULL,
                sale_price  REAL  NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                time_id  INTEGER NOT NULL,
                cons_id  INTEGER NOT NULL,
                qty      INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (time_id) REFERENCES time_rec(id),
                FOREIGN KEY (cons_id) REFERENCES consumables(id)
            )
        """)

        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_orders_time ON orders(time_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_orders_cons ON orders(cons_id)"
        )
        con.commit()

init_db()


# 3.  Flask API

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

@app.post("/api/orders")
def save_order():
    data = request.get_json(force=True)

    # timestamp > (day, time)
    ts_raw = data.get("timestamp")
    if ts_raw is None:
        return jsonify({"error": "timestamp missing"}), 400

    day_str, time_str = parse_and_round(ts_raw)

    # order lines
    lines = data.get("lines", [])
    if not lines:
        return jsonify({"error": "lines empty"}), 400

    with get_db_conn() as con:
        cur = con.cursor()

        # ensure / insert the (day,time) record, get its id
        cur.execute(
            "SELECT id FROM time_rec WHERE day=? AND time=?",
            (day_str, time_str)
        )
        row = cur.fetchone()
        if row:
            time_id = row[0]
        else:
            cur.execute(
                "INSERT INTO time_rec (day, time) VALUES (?, ?)",
                (day_str, time_str)
            )
            time_id = cur.lastrowid

        # insert each line item
        cur.executemany(
            """
            INSERT INTO orders (time_id, cons_id, qty)
            VALUES (?, ?, ?)
            """,
            [
                (time_id, line["cons_id"], line.get("qty", 1))
                for line in lines
            ]
        )

        con.commit()

    return jsonify({"status": "ok", "time_id": time_id}), 201


# 4.  Run

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
