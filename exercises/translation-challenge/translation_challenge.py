import sqlite3
import pandas as pd


# Sales data that we'll use for both SQL and pandas.
sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]

columns = [
    "product",
    "category",
    "unit_price",
    "quantity",
    "quarter"
]

# Create a pandas DataFrame using the sales data.
df = pd.DataFrame(sales_data, columns=columns)

# Create an in-memory SQLite database.
conn = sqlite3.connect(":memory:")

# Create the sales table.
conn.execute("""
CREATE TABLE sales (
    product TEXT,
    category TEXT,
    unit_price REAL,
    quantity INTEGER,
    quarter TEXT
)
""")

# Add all of the sales data to the SQL table.
conn.executemany("""
INSERT INTO sales (
    product,
    category,
    unit_price,
    quantity,
    quarter
)
VALUES (?, ?, ?, ?, ?)
""", sales_data)

conn.commit()

# Question 1: What is the total revenue per product?
print("=== Question 1: Total Revenue Per Product ===")

# SQL version
sql_revenue = conn.execute("""
SELECT
    product,
    SUM(unit_price * quantity) AS total_revenue
FROM sales
GROUP BY product
""").fetchall()

print("\nSQL:")
for product, revenue in sql_revenue:
    print(f"{product}: ${revenue:.2f}")

# pandas version
pandas_revenue = (
    df.assign(revenue=df["unit_price"] * df["quantity"])
      .groupby("product")["revenue"]
      .sum()
)

print("\npandas:")
print(pandas_revenue)

print()

# Question 2: Which quarter had the highest total quantity sold?
print("=== Question 2: Quarter With Highest Quantity Sold ===")

# SQL version
sql_quarter = conn.execute("""
SELECT
    quarter,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY quarter
ORDER BY total_quantity DESC
LIMIT 1
""").fetchone()

print("\nSQL:")
print(f"{sql_quarter[0]}: {sql_quarter[1]} units")

# pandas version
pandas_quarter = (
    df.groupby("quarter")["quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(1)
)

print("\npandas:")
print(pandas_quarter)

print()

# Question 3: What is the average unit price per category?
print("=== Question 3: Average Unit Price Per Category ===")

# SQL version
sql_average = conn.execute("""
SELECT
    category,
    AVG(unit_price) AS average_price
FROM sales
GROUP BY category
""").fetchall()

print("\nSQL:")
for category, average_price in sql_average:
    print(f"{category}: ${average_price:.2f}")

# pandas version
pandas_average = (
    df.groupby("category")["unit_price"]
      .mean()
)

print("\npandas:")
print(pandas_average)

print()

# Question 4: Which products had total quantity over 200?
print("=== Question 4: Products With Total Quantity Over 200 ===")

# SQL version
sql_products = conn.execute("""
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
HAVING SUM(quantity) > 200
""").fetchall()

print("\nSQL:")
for product, total_quantity in sql_products:
    print(f"{product}: {total_quantity} units")

# pandas version
pandas_products = (
    df.groupby("product")["quantity"]
      .sum()
)

pandas_products = pandas_products[pandas_products > 200]

print("\npandas:")
print(pandas_products)

print()

# BONUS: Run a SQL query and load the result directly into a pandas DataFrame.
print("=== BONUS: pd.read_sql() ===")

bonus_df = pd.read_sql("""
SELECT
    product,
    SUM(unit_price * quantity) AS total_revenue
FROM sales
GROUP BY product
""", conn)

print(bonus_df)

conn.close()