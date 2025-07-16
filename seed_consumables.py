
"""
Seed the consumables table so its IDs, names, and prices
match the catalog hard-coded in app.js.
"""

import sqlite3
from contextlib import closing

DB_FILE = "pos.db"

# must line up with <script src="app.js"> catalog 
CATALOG = [
    # id, name, price, fb_type, category
    (1,   "Full English Plate",   10.5,   "F",     "Breakfast"),
    (2,   "Smoked Salmon & Scrambled Eggs on Sourdough",   9.8,   "F",     "Breakfast"),
    (3,   "Avocado-Chili Smash, Feta & Poached Egg",   8.9,   "F",     "Breakfast"),
    (4,   "Cinnamon Brioche French Toast",   7.5,   "F",     "Breakfast"),
    (5,   "Maple-Pecan Granola Bowl",   6.2,   "F",     "Breakfast"),
    (6,   "Breakfast Burrito with Chorizo",   8.4,   "F",     "Breakfast"),
    (7,   "Vegan \"Sunrise\" Tofu Scramble Wrap",   7.9,   "F",     "Breakfast"),
    (8,   "Buttermilk Pancakes, Berry Compote, Crème Fraîche",   7.8,   "F",     "Breakfast"),
    (9,   "Porridge with Honey, Banana & Seeds",   4.8,   "F",     "Breakfast"),
    (10,   "Chargrilled Rib-Eye Steak, Chimichurri, Fries",   23.5,   "F",     "Main Meals"),
    (11,   "Pan-Seared Sea Bass, Lemon-Caper Butter",   18.9,   "F",     "Main Meals"),
    (12,   "Slow-Cooked Lamb Shank, Rosemary Jus",   19.8,   "F",     "Main Meals"),
    (13,   "Wild-Mushroom Risotto, Truffle Oil",   14.6,   "F",     "Main Meals"),
    (14,   "Chicken Katsu Curry, Sticky Rice",   15.2,   "F",     "Main Meals"),
    (15,   "BBQ Jackfruit Burger, Sweet-Potato Fries",   13.4,   "F",     "Main Meals"),
    (16,   "Handmade Spinach & Ricotta Ravioli",   13.9,   "F",     "Main Meals"),
    (17,   "Pulled Pork Tacos (3) & Pico de Gallo",   14.2,   "F",     "Main Meals"),
    (18,   "Harissa-Roasted Cauliflower Steak, Tahini Drizzle",   12.8,   "F",     "Main Meals"),
    (19,   "Dark Chocolate Fondant, Vanilla Ice Cream",   7.6,   "F",     "Dessert"),
    (20,   "Classic Sticky Toffee Pudding",   6.9,   "F",     "Dessert"),
    (21,   "Lemon Posset, Shortbread Crumble",   6.5,   "F",     "Dessert"),
    (22,   "Salted Caramel Cheesecake",   6.8,   "F",     "Dessert"),
    (23,   "Affogato al Caffè",   5.2,   "F",     "Dessert"),
    (24,   "Eton Mess with Strawberries",   6.4,   "F",     "Dessert"),
    (25,   "Baked Apple & Cinnamon Crumble",   6.3,   "F",     "Dessert"),
    (26,   "Pistachio Gelato Trio",   5.8,   "F",     "Dessert"),
    (27,   "Vegan Chocolate-Avocado Mousse",   6,   "F",     "Dessert"),
    (28,   "Flat White",   3.2,   "B",     "Hot Drink"),
    (29,   "Cappuccino",   3,   "B",     "Hot Drink"),
    (30,   "Americano",   2.7,   "B",     "Hot Drink"),
    (31,   "Espresso (single)",   2.1,   "B",     "Hot Drink"),
    (32,   "Mocha",   3.4,   "B",     "Hot Drink"),
    (33,   "Matcha Latte",   3.6,   "B",     "Hot Drink"),
    (34,   "Loose-Leaf English Breakfast Tea",   2.4,   "B",     "Hot Drink"),
    (35,   "Earl Grey Tea",   2.5,   "B",     "Hot Drink"),
    (36,   "Fresh Mint & Honey Infusion",   2.7,   "B",     "Hot Drink"),
    (37,   "Fresh-Pressed Orange Juice",   3.5,   "B",     "Soft Drink"),
    (38,   "Homemade Elderflower Lemonade",   3.2,   "B",     "Soft Drink"),
    (39,   "Sparkling Apple & Ginger Fizz",   3.3,   "B",     "Soft Drink"),
    (40,   "Still Mineral Water (750 ml)",   2.9,   "B",     "Soft Drink"),
    (41,   "Sparkling Mineral Water (750 ml)",   3.1,   "B",     "Soft Drink"),
    (42,   "Cola (bottle)",   2.7,   "B",     "Soft Drink"),
    (43,   "Diet Cola (bottle)",   2.7,   "B",     "Soft Drink"),
    (44,   "Raspberry & Hibiscus Iced Tea",   3.4,   "B",     "Soft Drink"),
    (45,   "Coconut Water (can)",   3,   "B",     "Soft Drink"),
    (46,   "Draught Pale Ale (pint)",   5.8,   "B",     "Alcoholic"),
    (47,   "House Red Wine, 175 ml",   6.2,   "B",     "Alcoholic"),
    (48,   "House White Wine, 175 ml",   6.2,   "B",     "Alcoholic"),
    (49,   "Prosecco, 125 ml",   7,   "B",     "Alcoholic"),
    (50,   "Classic Gin & Tonic",   7.5,   "B",     "Alcoholic"),
    (51,   "Passion-Fruit Martini",   8.4,   "B",     "Alcoholic"),
    (52,   "Old Fashioned",   8.6,   "B",     "Alcoholic"),
    (53,   "Aperol Spritz",   7.8,   "B",     "Alcoholic"),
    (54,   "Alcohol-Free Lager (bottle)",   4.6,   "B",     "Alcoholic"),
]

def seed():
    with closing(sqlite3.connect(DB_FILE)) as con:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # wipe existing rows
        cur.execute("DELETE FROM consumables")

        cur.executemany(
            """
            INSERT INTO consumables (id, name, fb_type, cat,
                                     unit_price, sale_price)
            VALUES (?,  ?,  ?,  ?,  ?,  ?)
            """,
            [
                (cid, name, fb, cat, price, price)  # sale_price == list price (for now)
                for cid, name, price, fb, cat in CATALOG
            ]
        )

        con.commit()
    print(f"Seeded {len(CATALOG)} consumables into {DB_FILE}")

if __name__ == "__main__":
    seed()