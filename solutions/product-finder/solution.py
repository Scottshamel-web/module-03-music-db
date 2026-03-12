"""
Exercise: The Product Finder
Module 3 — Databases & SQL
Lesson 3 — Practice Exercise
Estimated time: 30 minutes

Objective: Write targeted SQL queries using WHERE, AND, ORDER BY, LIMIT, and LIKE
to find specific products in a database.
"""

import sqlite3

# ============================================================
# SETUP: Create and populate the products table
# ============================================================

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.execute("""
    CREATE TABLE products (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        category TEXT,
        price    REAL,
        rating   REAL,
        in_stock INTEGER  -- SQLite has no BOOLEAN; use 1=True, 0=False
    )
""")

products = [
    ("Laptop Pro",                 "Electronics",  1299.00, 4.7, 1),
    ("USB-C Hub",                  "Accessories",    49.99, 4.3, 1),
    ("Wireless Mouse",             "Accessories",    39.99, 4.6, 1),
    ("4K Monitor",                 "Electronics",   799.00, 4.8, 1),
    ("Budget Monitor",             "Electronics",   299.00, 4.1, 0),
    ("Mechanical Keyboard",        "Accessories",    89.99, 4.9, 1),
    ("Webcam HD",                  "Electronics",    79.99, 4.2, 0),
    ("Desk Lamp",                  "Accessories",    29.99, 3.8, 1),
    ("Bluetooth Speaker",          "Audio",          59.99, 4.5, 1),
    ("Noise-Cancelling Headphones","Audio",         249.99, 4.8, 1),
    ("Phone Stand",                "Accessories",    14.99, 4.0, 1),
    ("Smart Monitor",              "Electronics",   499.00, 4.4, 1),
]

conn.executemany(
    "INSERT INTO products (name, category, price, rating, in_stock) VALUES (?, ?, ?, ?, ?)",
    products
)
conn.commit()

# ============================================================
# QUERY 1: Out-of-stock products
# WHERE filters rows — only rows where in_stock = 0 are returned
# ============================================================
print("1. Products currently out of stock:")
print("-" * 45)
rows = conn.execute("""
    SELECT name, category
    FROM products
    WHERE in_stock = 0
""").fetchall()
for r in rows:
    print(f"   {r['name']} ({r['category']})")

# ============================================================
# QUERY 2: High-rated AND affordable
# AND requires BOTH conditions to be true — think of it as an intersection
# ============================================================
print("\n2. Rating >= 4.5 AND price < $100:")
print("-" * 45)
rows = conn.execute("""
    SELECT name, rating, price
    FROM products
    WHERE rating >= 4.5 AND price < 100
    ORDER BY rating DESC
""").fetchall()
for r in rows:
    print(f"   {r['name']:<30} ⭐ {r['rating']}  ${r['price']:.2f}")

# ============================================================
# QUERY 3: Most expensive Accessories
# ORDER BY DESC sorts highest first; LIMIT caps the result count
# ============================================================
print("\n3. 3 most expensive Accessories (sorted by price):")
print("-" * 45)
rows = conn.execute("""
    SELECT name, price
    FROM products
    WHERE category = 'Accessories'
    ORDER BY price DESC
    LIMIT 3
""").fetchall()
for i, r in enumerate(rows, 1):
    print(f"   {i}. {r['name']:<30} ${r['price']:.2f}")

# ============================================================
# QUERY 4: Partial name match with LIKE
# LIKE does pattern matching: % is a wildcard meaning "any characters"
# 'Monitor%' = starts with Monitor; '%Monitor%' = contains Monitor anywhere
# ============================================================
print("\n4. Products with 'Monitor' in the name:")
print("-" * 45)
rows = conn.execute("""
    SELECT name, category, price, rating, in_stock
    FROM products
    WHERE name LIKE '%Monitor%'
""").fetchall()
for r in rows:
    stock = "In Stock" if r['in_stock'] else "Out of Stock"
    print(f"   {r['name']:<30} {r['category']:<12} ${r['price']:.2f}  ⭐{r['rating']}  {stock}")

# ============================================================
# QUERY 5: Multiple filters + multi-column sort
# ORDER BY category, price sorts by category first, then by price within each category
# ============================================================
print("\n5. In-stock products NOT in Accessories (sorted by category, then price):")
print("-" * 60)
rows = conn.execute("""
    SELECT name, category, price
    FROM products
    WHERE category != 'Accessories' AND in_stock = 1
    ORDER BY category, price
""").fetchall()
for r in rows:
    print(f"   {r['name']:<35} {r['category']:<15} ${r['price']:.2f}")

conn.close()
