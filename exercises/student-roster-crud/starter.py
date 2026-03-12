"""
Exercise: Student Roster CRUD
Module 3 | Lesson 2 | ~30 min

Objective:
  Build the four core CRUD operations (Create, Read, Update, Delete) as
  Python functions that wrap parameterized SQL statements.
"""

import sqlite3


# ── Setup helpers (provided — do not modify) ──────────────────────────────────

def create_connection() -> sqlite3.Connection:
    """Return a connection to an in-memory database with the students table."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            grade INTEGER NOT NULL,
            gpa   REAL    DEFAULT 0.0
        )
    """)
    conn.commit()
    return conn


def print_roster(conn: sqlite3.Connection) -> None:
    """Print all students in a formatted table."""
    rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
    if not rows:
        print("  (roster is empty)")
        return
    print(f"  {'ID':<4} {'Name':<20} {'Grade':<6} {'GPA'}")
    print("  " + "-" * 40)
    for row in rows:
        print(f"  {row['id']:<4} {row['name']:<20} {row['grade']:<6} {row['gpa']:.2f}")


# ── CRUD functions — implement these ──────────────────────────────────────────

def add_student(conn: sqlite3.Connection, name: str, grade: int, gpa: float) -> int:
    """
    Insert a new student and return their auto-assigned id.

    Args:
        conn:  active database connection
        name:  student's full name
        grade: grade level (e.g. 9, 10, 11, 12)
        gpa:   grade point average (0.0 – 4.0)

    Returns:
        The id of the newly inserted row.
    """
    # TODO: execute an INSERT statement using parameterized values
    # Hint: cursor = conn.execute("INSERT INTO students ...")
    #       conn.commit()
    #       return cursor.lastrowid
    pass


def get_all_students(conn: sqlite3.Connection) -> list:
    """
    Return all rows from the students table as a list of Row objects.
    Order by id ascending.
    """
    # TODO: execute a SELECT * query and return all results
    pass


def get_student_by_id(conn: sqlite3.Connection, student_id: int):
    """
    Return a single student row by id, or None if not found.
    """
    # TODO: execute SELECT with WHERE id = ? and return one row (or None)
    pass


def update_student_gpa(conn: sqlite3.Connection, student_id: int, new_gpa: float) -> bool:
    """
    Update the GPA for the student with the given id.

    Returns:
        True if a row was updated, False if no student with that id exists.
    """
    # TODO: execute an UPDATE statement
    # Hint: check cursor.rowcount to know if any row was actually changed
    pass


def delete_student(conn: sqlite3.Connection, student_id: int) -> bool:
    """
    Delete the student with the given id.

    Returns:
        True if a row was deleted, False if no student with that id exists.
    """
    # TODO: execute a DELETE statement and check rowcount
    pass


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    conn = create_connection()

    # Create
    print("Adding students...")
    id1 = add_student(conn, "Alice Johnson", 11, 3.8)
    id2 = add_student(conn, "Bob Williams",  10, 3.2)
    id3 = add_student(conn, "Carol Davis",   12, 3.9)
    print_roster(conn)

    # Read
    print("\nLooking up student by id...")
    student = get_student_by_id(conn, id1)
    print(f"  Found: {student['name']}, Grade {student['grade']}, GPA {student['gpa']}")

    # Update
    print("\nUpdating Alice's GPA to 4.0...")
    update_student_gpa(conn, id1, 4.0)
    print_roster(conn)

    # Delete
    print("\nDeleting Bob...")
    delete_student(conn, id2)
    print_roster(conn)

    conn.close()

    # Expected output:
    # Adding students...
    #   ID   Name                 Grade  GPA
    #   ----------------------------------------
    #   1    Alice Johnson        11     3.80
    #   2    Bob Williams         10     3.20
    #   3    Carol Davis          12     3.90
    #
    # Looking up student by id...
    #   Found: Alice Johnson, Grade 11, GPA 3.8
    #
    # Updating Alice's GPA to 4.0...
    #   ID   Name                 Grade  GPA
    #   ----------------------------------------
    #   1    Alice Johnson        11     4.00
    #   ...
    #
    # Deleting Bob...
    #   ID   Name                 Grade  GPA
    #   ----------------------------------------
    #   1    Alice Johnson        11     4.00
    #   3    Carol Davis          12     3.90
