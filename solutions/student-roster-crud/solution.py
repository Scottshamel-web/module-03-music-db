"""
Exercise: Student Roster CRUD
Module 3 — Databases & SQL
Lesson 2 — Practice Exercise
Estimated time: 30 minutes

Objective: Build the four fundamental database operations (Create, Read, Update,
Delete) as reusable Python functions. Understand why parameterized queries matter.
"""

import sqlite3

# ============================================================
# DATABASE SETUP
# ============================================================

def create_connection():
    """Create and return an in-memory SQLite connection with the students table."""
    conn = sqlite3.connect(":memory:")
    # row_factory lets us access columns by name (row["name"]) instead of index (row[0])
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            grade INTEGER NOT NULL,
            gpa   REAL
        )
    """)
    conn.commit()
    return conn

# ============================================================
# CRUD FUNCTIONS
# ============================================================

def add_student(conn, name, grade, gpa):
    """INSERT a new student. Returns the new student's id.

    Uses ? placeholders (parameterized query) — NEVER use f-strings or % formatting
    to build SQL queries. Parameterized queries prevent SQL injection attacks where
    a malicious name like "'; DROP TABLE students; --" could destroy your database.
    """
    cursor = conn.execute(
        "INSERT INTO students (name, grade, gpa) VALUES (?, ?, ?)",
        (name, grade, gpa)
    )
    conn.commit()
    return cursor.lastrowid

def get_all_students(conn):
    """SELECT all students, ordered by name. Returns a list of Row objects."""
    return conn.execute("SELECT * FROM students ORDER BY name").fetchall()

def get_student_by_id(conn, student_id):
    """SELECT a single student by id. Returns a Row object or None."""
    return conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)     # Note the trailing comma — single-item tuples need it
    ).fetchone()

def update_student_gpa(conn, student_id, new_gpa):
    """UPDATE the GPA for a specific student. Returns number of rows changed."""
    cursor = conn.execute(
        "UPDATE students SET gpa = ? WHERE id = ?",
        (new_gpa, student_id)
    )
    conn.commit()
    return cursor.rowcount

def delete_student(conn, student_id):
    """DELETE a student by id. Returns number of rows deleted."""
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    return cursor.rowcount

# ============================================================
# HELPER
# ============================================================

def print_roster(conn):
    """Print all students in a formatted table."""
    students = get_all_students(conn)
    if not students:
        print("  (no students)")
        return
    print(f"  {'ID':<4} {'Name':<20} {'Grade':<7} {'GPA'}")
    print("  " + "-" * 40)
    for s in students:
        gpa_str = f"{s['gpa']:.2f}" if s['gpa'] is not None else "N/A"
        print(f"  {s['id']:<4} {s['name']:<20} {s['grade']:<7} {gpa_str}")

# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    conn = create_connection()

    # CREATE — add four students
    print("Adding students...")
    add_student(conn, "Alice Chen", 11, 3.9)
    add_student(conn, "Bob Martinez", 10, 3.2)
    add_student(conn, "Diana Prince", 12, 3.7)
    add_student(conn, "Carlos Rivera", 11, 2.8)

    print("\nAll students after adding:")
    print_roster(conn)

    # READ — look up a specific student
    print("\nLooking up student with id=2:")
    student = get_student_by_id(conn, 2)
    print(f"  Found: {student['name']}, Grade {student['grade']}, GPA {student['gpa']}")

    # UPDATE — improve Bob's GPA
    print("\nUpdating Bob's GPA to 3.5...")
    rows_changed = update_student_gpa(conn, 2, 3.5)
    print(f"  {rows_changed} row(s) updated")

    # DELETE — remove Carlos
    print("\nDeleting Carlos Rivera (id=4)...")
    rows_deleted = delete_student(conn, 4)
    print(f"  {rows_deleted} row(s) deleted")

    print("\nFinal roster:")
    print_roster(conn)

    conn.close()
