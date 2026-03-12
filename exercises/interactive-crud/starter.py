"""
Exercise: The Interactive CRUD App
Module 3 | Lesson 2 Stretch | ~35 min

Objective:
  Wrap the CRUD functions from the Student Roster exercise in a
  menu-driven CLI loop so a user can manage the roster interactively.
"""

import sqlite3


# ── Setup (provided — do not modify) ──────────────────────────────────────────

def create_connection() -> sqlite3.Connection:
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


# ── CRUD helpers (provided — do not modify) ───────────────────────────────────
# These are fully implemented so you can focus on the menu handlers below.

def add_student(conn, name, grade, gpa):
    cursor = conn.execute(
        "INSERT INTO students (name, grade, gpa) VALUES (?, ?, ?)",
        (name, grade, gpa)
    )
    conn.commit()
    return cursor.lastrowid


def get_all_students(conn):
    return conn.execute("SELECT * FROM students ORDER BY id").fetchall()


def get_student_by_id(conn, student_id):
    return conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()


def update_student_gpa(conn, student_id, new_gpa):
    cursor = conn.execute(
        "UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, student_id)
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_student(conn, student_id):
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    return cursor.rowcount > 0


def print_roster(conn):
    rows = get_all_students(conn)
    if not rows:
        print("  (roster is empty)")
        return
    print(f"  {'ID':<4} {'Name':<20} {'Grade':<6} {'GPA'}")
    print("  " + "-" * 40)
    for row in rows:
        print(f"  {row['id']:<4} {row['name']:<20} {row['grade']:<6} {row['gpa']:.2f}")


# ── Menu handlers — implement these ───────────────────────────────────────────

def handle_add(conn: sqlite3.Connection) -> None:
    """
    Prompt the user for a student's name, grade, and GPA, then insert them.
    Print a confirmation message after adding.
    """
    # TODO: use input() to collect name, grade (int), gpa (float)
    # TODO: call add_student() and print "Added [name] with id=[id]"
    pass


def handle_view(conn: sqlite3.Connection) -> None:
    """
    Display the full roster using print_roster().
    """
    # TODO: call print_roster(conn)
    pass


def handle_update(conn: sqlite3.Connection) -> None:
    """
    Prompt the user for a student ID and a new GPA, then update.
    Print a success or "not found" message.
    """
    # TODO: use input() to collect student_id (int) and new_gpa (float)
    # TODO: call update_student_gpa() and print outcome
    pass


def handle_delete(conn: sqlite3.Connection) -> None:
    """
    Prompt the user for a student ID and delete that student.
    Print a success or "not found" message.
    """
    # TODO: use input() to collect student_id (int)
    # TODO: call delete_student() and print outcome
    pass


# ── Menu loop (provided — do not modify) ──────────────────────────────────────

def run_menu(conn: sqlite3.Connection) -> None:
    """Run the interactive menu loop until the user chooses to quit."""
    while True:
        print("\n=== Student Roster ===")
        print("1. Add student")
        print("2. View all students")
        print("3. Update GPA")
        print("4. Delete student")
        print("5. Quit")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            handle_add(conn)
        elif choice == "2":
            handle_view(conn)
        elif choice == "3":
            handle_update(conn)
        elif choice == "4":
            handle_delete(conn)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice — enter 1 through 5.")


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Non-interactive scripted demo to verify your handlers work
    conn = create_connection()

    # Seed some data directly
    add_student(conn, "Alice Johnson", 11, 3.8)
    add_student(conn, "Bob Williams",  10, 3.2)
    add_student(conn, "Carol Davis",   12, 3.9)

    print("Initial roster:")
    handle_view(conn)

    # To test the full interactive loop, call run_menu(conn) here:
    # run_menu(conn)

    conn.close()
