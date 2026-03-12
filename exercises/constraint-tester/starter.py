"""
Exercise: The Constraint Tester
Module 3 | Lesson 1 Stretch | ~30 min

Objective:
  Intentionally trigger four types of database constraint violations and
  observe how SQLite reports each one. Understanding constraint errors is
  essential for building reliable applications.
"""

import sqlite3


def make_db() -> sqlite3.Connection:
    """
    Build and return an in-memory database with constrained tables.
    This setup code is provided — do not modify it.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE departments (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE employees (
            id            INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE,
            salary        REAL CHECK(salary >= 0),
            department_id INTEGER REFERENCES departments(id)
        );

        INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Marketing');
        INSERT INTO employees VALUES (1, 'Alice', 'alice@co.com', 95000, 1);
    """)
    conn.commit()
    return conn


# ── Task 1: PRIMARY KEY violation ─────────────────────────────────────────────
# Attempt to insert a row with an id that already exists.
# Expected error: UNIQUE constraint failed: employees.id
def task1_primary_key(conn: sqlite3.Connection) -> None:
    print("\n--- Task 1: PRIMARY KEY violation ---")
    try:
        # TODO: INSERT into employees with id=1 (already exists)
        pass
    except sqlite3.IntegrityError as e:
        print(f"Caught expected error: {e}")


# ── Task 2: UNIQUE constraint violation ───────────────────────────────────────
# Attempt to insert an employee with an email that already exists.
# Expected error: UNIQUE constraint failed: employees.email
def task2_unique(conn: sqlite3.Connection) -> None:
    print("\n--- Task 2: UNIQUE constraint violation ---")
    try:
        # TODO: INSERT into employees with email='alice@co.com' (already taken)
        pass
    except sqlite3.IntegrityError as e:
        print(f"Caught expected error: {e}")


# ── Task 3: CHECK constraint violation ────────────────────────────────────────
# Attempt to insert an employee with a negative salary.
# Expected error: CHECK constraint failed: salary >= 0
def task3_check(conn: sqlite3.Connection) -> None:
    print("\n--- Task 3: CHECK constraint violation ---")
    try:
        # TODO: INSERT into employees with salary = -5000
        pass
    except sqlite3.IntegrityError as e:
        print(f"Caught expected error: {e}")


# ── Task 4: FOREIGN KEY violation ─────────────────────────────────────────────
# Attempt to insert an employee referencing a department that doesn't exist.
# Expected error: FOREIGN KEY constraint failed
def task4_foreign_key(conn: sqlite3.Connection) -> None:
    print("\n--- Task 4: FOREIGN KEY violation ---")
    try:
        # TODO: INSERT into employees with department_id=999 (does not exist)
        pass
    except sqlite3.IntegrityError as e:
        print(f"Caught expected error: {e}")


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    conn = make_db()

    task1_primary_key(conn)
    task2_unique(conn)
    task3_check(conn)
    task4_foreign_key(conn)

    conn.close()
    print("\nAll constraint tests complete.")

    # Expected output:
    # --- Task 1: PRIMARY KEY violation ---
    # Caught expected error: UNIQUE constraint failed: employees.id
    #
    # --- Task 2: UNIQUE constraint violation ---
    # Caught expected error: UNIQUE constraint failed: employees.email
    #
    # --- Task 3: CHECK constraint violation ---
    # Caught expected error: CHECK constraint failed: salary >= 0
    #
    # --- Task 4: FOREIGN KEY violation ---
    # Caught expected error: FOREIGN KEY constraint failed
