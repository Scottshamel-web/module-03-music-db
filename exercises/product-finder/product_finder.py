import sqlite3


# I'm using an in-memory database for this exercise.
# It gets created when the script starts and disappears when it finishes.
conn = sqlite3.connect(":memory:")

# This lets me access results using column names instead of position numbers.
conn.row_factory = sqlite3.Row


def create_table():
    """Create the products table."""

    conn.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            rating REAL,
            in_stock INTEGER NOT NULL
        )
    """)

    conn.commit()


def insert_products():
    """Add some sample products so the queries have data to search."""

    products = [
        ("Wireless Mouse", "Accessories", 29.99, 4.6, 1),
        ("Mechanical Keyboard", "Accessories", 89.99, 4.8, 1),
        ("USB-C Hub", "Accessories", 49.99, 4.4, 0),
        ("Laptop Stand", "Accessories", 59.99, 4.7, 1),
        ("Premium Dock", "Accessories", 149.99, 4.9, 1),
        ("Gaming Monitor", "Electronics", 399.99, 4.8, 1),
        ("Portable Monitor", "Electronics", 199.99, 4.5, 0),
        ("Office Monitor", "Electronics", 249.99, 4.3, 1),
        ("Python Book", "Books", 39.99, 4.9, 1),
        ("Desk Lamp", "Home", 34.99, 4.6, 1),
    ]

    # executemany lets me insert all of the products using one SQL statement.
    # The ? placeholders keep the values separate from the SQL itself.
    conn.executemany(
        """
        INSERT INTO products
            (name, category, price, rating, in_stock)
        VALUES (?, ?, ?, ?, ?)
        """,
        products
    )

    conn.commit()


def print_rows(rows):
    """Print every row in a readable way."""

    for row in rows:
        print(dict(row))


if __name__ == "__main__":
    create_table()
    insert_products()

    # ------------------------------------------------------------
    # 1. Which products are out of stock?
    # 0 means false/out of stock, while 1 means true/in stock.
    # ------------------------------------------------------------
    print("\n1. OUT OF STOCK PRODUCTS")

    cursor = conn.execute("""
        SELECT name, category
        FROM products
        WHERE in_stock = 0
    """)

    print_rows(cursor.fetchall())


    # ------------------------------------------------------------
    # 2. Products rated 4.5+ that also cost less than $100.
    # AND means both conditions have to be true.
    # ------------------------------------------------------------
    print("\n2. RATING 4.5 OR HIGHER AND UNDER $100")

    cursor = conn.execute("""
        SELECT name, rating, price
        FROM products
        WHERE rating >= 4.5
          AND price < 100
    """)

    print_rows(cursor.fetchall())


    # ------------------------------------------------------------
    # 3. The 3 most expensive Accessories products.
    # DESC puts the highest prices first, then LIMIT keeps only 3.
    # ------------------------------------------------------------
    print("\n3. TOP 3 MOST EXPENSIVE ACCESSORIES")

    cursor = conn.execute("""
        SELECT name, price
        FROM products
        WHERE category = 'Accessories'
        ORDER BY price DESC
        LIMIT 3
    """)

    print_rows(cursor.fetchall())


    # ------------------------------------------------------------
    # 4. Products with the word "Monitor" anywhere in the name.
    # The % signs mean there can be text before or after Monitor.
    # ------------------------------------------------------------
    print("\n4. PRODUCTS WITH 'MONITOR' IN THE NAME")

    cursor = conn.execute("""
        SELECT *
        FROM products
        WHERE name LIKE '%Monitor%'
    """)

    print_rows(cursor.fetchall())


    # ------------------------------------------------------------
    # 5. Products that are not Accessories and are currently in stock.
    # First sort alphabetically by category, then by price.
    # ------------------------------------------------------------
    print("\n5. IN-STOCK PRODUCTS NOT IN ACCESSORIES")

    cursor = conn.execute("""
        SELECT name, category, price
        FROM products
        WHERE category != 'Accessories'
          AND in_stock = 1
        ORDER BY category, price
    """)

    print_rows(cursor.fetchall())


    # Always close the database connection when we're finished.
    conn.close()