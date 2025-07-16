# data_generator.py
import sqlite3
from contextlib import closing
from datetime import datetime, date, timedelta
import numpy as np
from zoneinfo import ZoneInfo

DB_FILE = "pos.db"
LOCAL_TZ = ZoneInfo("Europe/London")

# 1. Helper: build the per-slot mean curve for a given weekday

def build_mean_curve(weekday, times):
    """
    Return an array of expected orders per 30-min slot for
    the given weekday (0=Mon … 6=Sun).
    """
    # meal times ((24h) hours)
    peaks  = np.array([10, 14, 18])
    # base heights      
    amps   = np.array([50, 45, 31])
    sigma  = 1.0
    weekend_global = 1.2
    # Sunday breakfast boost
    special = {(6, 0): 1.2}

    if weekday >= 5: # Sat/Sun                    
        amps = amps * weekend_global

    for (wd, idx), factor in special.items():
        if wd == weekday:
            amps[idx] *= factor

    curve = np.zeros_like(times, dtype=float)
    for a, p in zip(amps, peaks):
        curve += a * np.exp(-0.5 * ((times - p) / sigma) ** 2)

    return curve.clip(min=0)

# 2. Main entry point

def generateData(start_date, end_date, db_path: str = DB_FILE):
    """
    Populate tables (time_rec and orders) with synthetic data between
    start_date and end_date (inclusive).
    """
    # normalise
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).date()
    if isinstance(end_date, str):
        end_date   = datetime.fromisoformat(end_date).date()

    half_hours = np.arange(8.0, 23.5, 0.5)
    rng        = np.random.default_rng()

    with closing(sqlite3.connect(db_path)) as con:
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()

        cons_ids = [int(row[0]) for row in cur.execute("SELECT id FROM consumables")]
        if not cons_ids:
            raise RuntimeError("No rows in consumables table (check seed)")

        d = start_date
        while d <= end_date:
            weekday = d.weekday()
            mu_curve = build_mean_curve(weekday, half_hours)

            for hour_val, mu in zip(half_hours, mu_curve):
                # draw how many orders in this slot
                n_orders = rng.poisson(mu)
                if n_orders == 0:
                    continue

                # slot label HH:MM
                h   = int(hour_val)
                m   = 30 if abs(hour_val - h - 0.5) < 1e-6 else 0
                t_str = f"{h:02d}:{m:02d}"

                # find/create time_rec row
                cur.execute(
                    "SELECT id FROM time_rec WHERE day=? AND time=?",
                    (d.isoformat(), t_str)
                )
                row = cur.fetchone()
                if row:
                    time_id = row[0]
                else:
                    cur.execute(
                        "INSERT INTO time_rec (day, time) VALUES (?,?)",
                        (d.isoformat(), t_str)
                    )
                    time_id = cur.lastrowid

                # build N random line items (qty fixed at 1)
                line_rows = [
                    (int(time_id), int(rng.choice(cons_ids)), 1)    # force pure ints
                    for _ in range(n_orders)
                ]
                try:
                    cur.executemany(
                        "INSERT INTO orders (time_id, cons_id, qty) VALUES (?,?,?)",
                        line_rows
                    )
                except sqlite3.IntegrityError as e:
                    print("FK fail on", line_rows[:5], "…")
                    raise

            d += timedelta(days=1)

        con.commit()
    print(f"Inserted synthetic data for {start_date} → {end_date}")

# 3. Run from CLI one-off

if __name__ == "__main__":
    generateData("2025-07-01", "2025-07-15")
