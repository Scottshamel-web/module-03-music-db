"""
Exercise: The Interactive CRUD App
Module 3 — Databases & SQL
Lesson 2 — Stretch Challenge
Estimated time: 35 minutes

Objective: Turn the student roster CRUD functions into a menu-driven CLI app.
Understand the loop-until-quit pattern used in many command-line tools.
"""

import sqlite3

# ============================================================
# DATABASE SETUP (same schema as the practice exercise)
# ============================================================

def create_connection():
    conn = sqlite3.connect(":memory:")
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

def add_student(conn, name, grade, gpa):
    cursor = conn.execute(
        "INSERT INTO students (name, grade, gpa) VALUES (?, ?, ?)",
        (name, grade, gpa)
    )
    conn.commit()
    return cursor.lastrowid

def get_all_students(conn):
    return conn.execute("SELECT * FROM students ORDER BY name").fetchall()

def update_student_gpa(conn, student_id, new_gpa):
    cursor = conn.execute(
        "UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, student_id)
    )
    conn.commit()
    return cursor.rowcount

def delete_student(conn, student_id):
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    return cursor.rowcount

# ============================================================
# MENU HANDLER FUNCTIONS
# ============================================================

def print_roster(conn):
    students = get_all_students(conn)
    if not students:
        print("  (no students in roster)")
        return
    print(f"\n  {'ID':<4} {'Name':<20} {'Grade':<7} {'GPA'}")
    print("  " + "-" * 40)
    for s in students:
        gpa_str = f"{s['gpa']:.2f}" if s['gpa'] is not None else "N/A"
        print(f"  {s['id']:<4} {s['name']:<20} {s['grade']:<7} {gpa_str}")

def handle_add(conn):
    """Prompt for student details and add to the roster."""
    name = input("  Student name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return
    try:
        grade = int(input("  Grade (9-12): ").strip())
        gpa_input = input("  GPA (leave blank if unknown): ").strip()
        gpa = float(gpa_input) if gpa_input else None
    except ValueError:
        print("  Invalid grade or GPA. Please enter numbers.")
        return
    new_id = add_student(conn, name, grade, gpa)
    print(f"  Added '{name}' with id={new_id}.")

def handle_view(conn):
    """Display all students."""
    print_roster(conn)

def handle_update(conn):
    """Prompt for student ID and new GPA, then update."""
    try:
        student_id = int(input("  Student ID to update: ").strip())
        new_gpa = float(input("  New GPA: ").strip())
    except ValueError:
        print("  Invalid input. Please enter numbers.")
        return
    rows = update_student_gpa(conn, student_id, new_gpa)
    if rows == 0:
        print(f"  No student found with id={student_id}.")
    else:
        print(f"  Updated student {student_id} GPA to {new_gpa}.")

def handle_delete(conn):
    """Prompt for student ID and delete that student."""
    try:
        student_id = int(input("  Student ID to delete: ").strip())
    except ValueError:
        print("  Invalid input. Please enter a number.")
        return
    rows = delete_student(conn, student_id)
    if rows == 0:
        print(f"  No student found with id={student_id}.")
    else:
        print(f"  Student {student_id} deleted.")

# ============================================================
# INTERACTIVE MENU LOOP
# Loop-until-quit is a common CLI pattern:
# 1. Show the menu
# 2. Read the user's choice
# 3. Dispatch to the appropriate handler
# 4. Repeat until the user chooses to quit
# ============================================================

def run_menu(conn):
    """Run the interactive menu loop."""
    while True:
        print("\n=== Student Roster ===")
        print("1. Add a student")
        print("2. View all students")
        print("3. Update a student's GPA")
        print("4. Delete a student")
        print("5. Quit")
        choice = input("Choose an option (1-5): ").strip()

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
            print("Invalid choice. Please enter 1-5.")

# ============================================================
# SCRIPTED DEMO (runs automatically without interactive input)
# This shows the same behavior as the menu loop, but scripted
# so the file can be run and tested without keyboard input.
# Uncomment the run_menu() call at the bottom to go interactive.
# ============================================================

if __name__ == "__main__":
    conn = create_connection()

    print("=== Scripted Demo (non-interactive) ===\n")

    # Step 1: Add students
    print("Adding 3 students...")
    add_student(conn, "Alice Chen", 11, 3.9)
    add_student(conn, "Bob Martinez", 10, 3.2)
    add_student(conn, "Carlos Rivera", 12, 3.7)

    print("\nView all students:")
    print_roster(conn)

    # Step 2: Update GPA
    print("\nUpdating Bob (id=2) GPA to 3.6...")
    update_student_gpa(conn, 2, 3.6)

    # Step 3: Delete a student
    print("Deleting Carlos (id=3)...")
    delete_student(conn, 3)

    print("\nFinal roster:")
    print_roster(conn)

    conn.close()

    # To run interactively, uncomment the lines below:
    # conn = create_connection()
    # run_menu(conn)
    # conn.close()
