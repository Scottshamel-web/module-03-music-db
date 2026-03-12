"""
Exercise: The Constraint Tester
Module 3 — Databases & SQL
Lesson 1 — Stretch Challenge
Estimated time: 30 minutes

Objective: Understand what database constraints protect against by deliberately
triggering each type of violation and observing the error.
"""

import sqlite3

def make_db():
    """Helper: create a fresh in-memory database with constrained tables."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""
        CREATE TABLE artists (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL UNIQUE,
            genre TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE albums (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT NOT NULL,
            year      INTEGER CHECK(year > 0),
            artist_id INTEGER,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        )
    """)
    conn.commit()
    return conn

# ============================================================
# EXPERIMENT 1: UNIQUE constraint violation
# ============================================================
# UNIQUE means no two rows can have the same value in that column.
# Protects against: duplicate entries, data integrity issues.
print("=" * 55)
print("EXPERIMENT 1: UNIQUE constraint (duplicate artist name)")
print("=" * 55)

conn = make_db()
conn.execute("INSERT INTO artists (name, genre) VALUES ('Beatles', 'Rock')")
conn.commit()

try:
    conn.execute("INSERT INTO artists (name, genre) VALUES ('Beatles', 'Pop')")
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"  Error caught: {e}")
    print("  Why this matters: UNIQUE prevents two artists from having the same name.")
    print("  Real-world use: usernames, email addresses, ISBNs.\n")

conn.close()

# ============================================================
# EXPERIMENT 2: NOT NULL constraint violation
# ============================================================
# NOT NULL means the column must always have a value — NULL is rejected.
# Protects against: missing required data that your queries depend on.
print("=" * 55)
print("EXPERIMENT 2: NOT NULL constraint (missing artist name)")
print("=" * 55)

conn = make_db()
try:
    # name is NOT NULL — passing None here maps to SQL NULL
    conn.execute("INSERT INTO artists (name, genre) VALUES (NULL, 'Rock')")
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"  Error caught: {e}")
    print("  Why this matters: a nameless artist would break every query that displays names.")
    print("  Real-world use: user.email, product.price, order.customer_id.\n")

conn.close()

# ============================================================
# EXPERIMENT 3: FOREIGN KEY constraint violation
# ============================================================
# FOREIGN KEY means the value must exist in the referenced table.
# Protects against: orphaned records (albums with no real artist).
print("=" * 55)
print("EXPERIMENT 3: FOREIGN KEY constraint (invalid artist_id)")
print("=" * 55)

conn = make_db()
conn.execute("INSERT INTO artists (name, genre) VALUES ('Radiohead', 'Alternative')")
conn.commit()

try:
    # artist_id=999 doesn't exist in the artists table
    conn.execute("INSERT INTO albums (title, year, artist_id) VALUES ('OK Computer', 1997, 999)")
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"  Error caught: {e}")
    print("  Why this matters: you can't have an album without a real artist.")
    print("  Requires: PRAGMA foreign_keys = ON (SQLite doesn't enforce by default).")
    print("  Real-world use: orders.customer_id, posts.author_id, invoices.product_id.\n")

conn.close()

# ============================================================
# EXPERIMENT 4: CHECK constraint (with and without it)
# ============================================================
# CHECK defines a condition every row must satisfy.
# Protects against: logically invalid values that SQLite's types wouldn't catch.
print("=" * 55)
print("EXPERIMENT 4: CHECK constraint (invalid year)")
print("=" * 55)

# Part A: WITH CHECK constraint — negative year is rejected
conn = make_db()
conn.execute("INSERT INTO artists (name, genre) VALUES ('Beatles', 'Rock')")
conn.commit()

try:
    conn.execute("INSERT INTO albums (title, year, artist_id) VALUES ('Abbey Road', -1969, 1)")
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"  WITH CHECK — Error caught: {e}")
    print("  A negative year was correctly rejected by CHECK(year > 0).")

conn.close()

# Part B: WITHOUT CHECK constraint — SQLite accepts any integer, including negative
conn2 = sqlite3.connect(":memory:")
conn2.execute("""
    CREATE TABLE albums_no_check (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year  INTEGER   -- no CHECK constraint
    )
""")
conn2.execute("INSERT INTO albums_no_check (title, year) VALUES ('Oops', -1969)")
conn2.commit()

row = conn2.execute("SELECT * FROM albums_no_check").fetchone()
print(f"\n  WITHOUT CHECK — Inserted successfully: {row}")
print("  SQLite's INTEGER type accepts any integer, even nonsense values.")
print("  CHECK constraints add application-level logic on top of type constraints.")
print("  Real-world use: age >= 0, price > 0, rating BETWEEN 1 AND 5.")

conn2.close()
