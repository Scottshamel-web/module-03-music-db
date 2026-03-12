"""
Exercise: The Translation Challenge
Module 3 — Databases & SQL
Lesson 9 — Practice Exercise
Estimated time: 40 minutes

Objective: Solve the same analytical questions using both SQL and pandas side by side.
Seeing both approaches builds intuition for when each tool is the right choice.
"""

import sqlite3
import pandas as pd

# ============================================================
# SHARED DATA
# ============================================================
sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99,  89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99,  50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]
# columns: product, category, unit_price, quantity, quarter

# ============================================================
# SETUP: Load into SQLite
# ============================================================
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE sales (
        product    TEXT,
        category   TEXT,
        unit_price REAL,
        quantity   INTEGER,
        quarter    TEXT
    )
""")
conn.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sales_data)
conn.commit()

# ============================================================
# SETUP: Load into pandas
# ============================================================
df = pd.DataFrame(sales_data, columns=["product", "category", "unit_price", "quantity", "quarter"])
df["revenue"] = df["unit_price"] * df["quantity"]  # computed column used in several questions

print("=" * 60)

# ============================================================
# QUESTION 1: Total revenue per product
# SQL: SUM(unit_price * quantity), GROUP BY product
# Pandas: assign computed column, then groupby + sum
# ============================================================
print("Q1: Total revenue per product\n")

# SQL approach — compute revenue inline with multiplication
sql_result = conn.execute("""
    SELECT product, ROUND(SUM(unit_price * quantity), 2) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
""").fetchall()
print("  SQL result:")
for row in sql_result:
    print(f"    {row[0]:<12} ${row[1]:>8,.2f}")

# Pandas approach — groupby('product'), aggregate the revenue column
pandas_result = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
print("\n  Pandas result:")
for product, rev in pandas_result.items():
    print(f"    {product:<12} ${rev:>8,.2f}")

print()

# ============================================================
# QUESTION 2: Quarter with highest total quantity
# SQL: SUM + GROUP BY + ORDER BY DESC + LIMIT 1
# Pandas: groupby + sum + idxmax()
# ============================================================
print("Q2: Quarter with highest total quantity\n")

sql_result = conn.execute("""
    SELECT quarter, SUM(quantity) AS total_qty
    FROM sales
    GROUP BY quarter
    ORDER BY total_qty DESC
    LIMIT 1
""").fetchone()
print(f"  SQL result:    {sql_result[0]} with {sql_result[1]} units")

pandas_result = df.groupby("quarter")["quantity"].sum()
best_quarter = pandas_result.idxmax()
print(f"  Pandas result: {best_quarter} with {pandas_result[best_quarter]} units")

print()

# ============================================================
# QUESTION 3: Average unit price per category
# SQL: AVG + GROUP BY
# Pandas: groupby + mean
# ============================================================
print("Q3: Average unit price per category\n")

sql_result = conn.execute("""
    SELECT category, ROUND(AVG(unit_price), 2) AS avg_price
    FROM sales
    GROUP BY category
    ORDER BY avg_price DESC
""").fetchall()
print("  SQL result:")
for row in sql_result:
    print(f"    {row[0]:<15} ${row[1]:.2f}")

pandas_result = df.groupby("category")["unit_price"].mean().sort_values(ascending=False)
print("\n  Pandas result:")
for cat, price in pandas_result.items():
    print(f"    {cat:<15} ${price:.2f}")

print()

# ============================================================
# QUESTION 4: Products with total quantity > 200 across all quarters
# SQL: HAVING clause filters AFTER grouping
# Pandas: groupby + sum, then boolean filter
# ============================================================
print("Q4: Products with total quantity > 200 across all quarters\n")

sql_result = conn.execute("""
    SELECT product, SUM(quantity) AS total_qty
    FROM sales
    GROUP BY product
    HAVING total_qty > 200
    ORDER BY total_qty DESC
""").fetchall()
print("  SQL result:")
for row in sql_result:
    print(f"    {row[0]:<12} {row[1]} units")

pandas_result = df.groupby("product")["quantity"].sum()
filtered = pandas_result[pandas_result > 200].sort_values(ascending=False)
print("\n  Pandas result:")
for product, qty in filtered.items():
    print(f"    {product:<12} {qty} units")

print()

# ============================================================
# BONUS: pd.read_sql() — run a SQL query and get a DataFrame directly
# This is the bridge between the two worlds: write SQL, get pandas output.
# Useful when: you want SQL for the data transformation but pandas for the output.
# ============================================================
print("BONUS: pd.read_sql() — SQL query → pandas DataFrame directly\n")

revenue_df = pd.read_sql("""
    SELECT product, quarter, ROUND(unit_price * quantity, 2) AS revenue
    FROM sales
    ORDER BY revenue DESC
""", conn)

print("  Revenue per (product, quarter) via pd.read_sql():")
print(revenue_df.to_string(index=False))

conn.close()
