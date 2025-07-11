from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os, datetime

DB_FILE = "pos.db"

# DB bootstrap
def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    # Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT    NOT NULL
        )
    """)
    # Line-items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_lines (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id  INTEGER NOT NULL,
            item_id   INTEGER NOT NULL,
            item_name TEXT    NOT NULL,
            qty       INTEGER NOT NULL,
            price     REAL    NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)
    con.commit()
    con.close()

init_db()

# Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

def get_db_conn():
    return sqlite3.connect(DB_FILE)

@app.post("/api/orders")
def save_order():
    data = request.get_json(force=True)
    timestamp = data.get("timestamp")
    lines      = data.get("lines", [])

    con = get_db_conn()
    cur = con.cursor()

    # insert into orders
    cur.execute("INSERT INTO orders (timestamp) VALUES (?)", (timestamp,))
    order_id = cur.lastrowid

    # insert each line
    cur.executemany(
        """
        INSERT INTO order_lines
              (order_id, item_id, item_name, qty, price)
        VALUES (?,        ?,       ?,         ?,   ?)
        """,
        [
            (
                order_id,
                line["id"],
                line["name"],
                line["qty"],
                line["price"],
            )
            for line in lines
        ],
    )

    con.commit()
    con.close()
    return jsonify({"status": "ok", "order_id": order_id})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
