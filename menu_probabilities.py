from __future__ import annotations
import numpy as np

TIME_GRID = np.arange(8.0, 23.0, 0.5)

GROUP_SPECS = [
    dict(name="Breakfast",
         peaks=[10.5], sigma=3.0, amps=[10],
         start=8, end=12),

    dict(name="Main Meals",
         peaks=[15, 18.5, 21], sigma=1.0, amps=[10, 15, 5],
         start=11.5, end=23),

    dict(name="Dessert",
         peaks=[15.5, 19, 22], sigma=1.0, amps=[3, 5, 2],
         start=11.5, end=23),

    dict(name="Hot Drink",
         peaks=[8, 10, 14, 18], sigma=2.0, amps=[3, 7, 3, 3],
         start=8, end=23),

    dict(name="Soft Drink",
         peaks=[10, 14, 18.5, 22.5], sigma=2.0, amps=[10, 7, 15, 11],
         start=8, end=23),

    dict(name="Alcoholic",
         peaks=[10, 14, 18.5, 22.5], sigma=1.5, amps=[3, 7, 15, 13],
         start=8, end=23),
]

def _curve(times: np.ndarray,
           peaks: list[float],
           amps:  list[float],
           sigma: float) -> np.ndarray:
    """Gaussian mixture evaluated on times."""
    c = np.zeros_like(times, dtype=float)
    for a, p in zip(amps, peaks):
        c += a * np.exp(-0.5 * ((times - p) / sigma) ** 2)
    return c

# probability matrix 

_counts = np.zeros((TIME_GRID.size, len(GROUP_SPECS)), dtype=float)

for col, spec in enumerate(GROUP_SPECS):
    mask = (TIME_GRID >= spec["start"]) & (TIME_GRID < spec["end"])
    _counts[mask, col] = _curve(
        TIME_GRID[mask],
        spec["peaks"],
        spec["amps"],
        spec["sigma"],
    )

_totals = _counts.sum(axis=1, keepdims=True)
with np.errstate(divide="ignore", invalid="ignore"):
    _probs = np.divide(_counts, _totals, where=_totals > 0)

_GROUP_NAMES = [spec["name"] for spec in GROUP_SPECS]
_rng = np.random.default_rng()

# api

def get_consumable(time: float | str) -> str:
    """
    Parameters
    ----------
    time : float | str
        Either a decimal hour (e.g. 15.5) or "HH:MM".

    Returns
    -------
    str
        A randomly selected menu group, weighted by P(group | time).
    """
    
    if isinstance(time, str):
        hh, mm = map(int, time.split(":"))
        time = hh + mm / 60.0
    time = float(time)

    idx = int(np.clip(np.round((time - TIME_GRID[0]) * 2), 0, TIME_GRID.size - 1))

    return _rng.choice(_GROUP_NAMES, p=_probs[idx])

# self test
if __name__ == "__main__":
    for t in (9.0, 11.0, 15.0, 19.0, 22.0):
        print(f"{t:04.1f}  :  {get_consumable(t)}")
