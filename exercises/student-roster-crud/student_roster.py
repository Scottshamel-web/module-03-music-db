import sqlite3


# Connect to school.db.
# SQLite will create the file automatically if it does not exist.
conn = sqlite3.connect("school.db")

# Let us access columns by name.
conn.row_factory = sqlite3.Row


def create_table():
    """Create the students table if it does not already exist."""

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            gpa REAL
        )
    """)

    conn.commit()


def add_student(name, grade, gpa):
    """Insert a new student."""

    conn.execute(
        "INSERT INTO students (name, grade, gpa) VALUES (?, ?, ?)",
        (name, grade, gpa)
    )

    conn.commit()


def get_all_students():
    """Return all students."""

    cursor = conn.execute(
        "SELECT * FROM students ORDER BY id"
    )

    return cursor.fetchall()


def get_student_by_id(student_id):
    """Return one student by ID."""

    cursor = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    return cursor.fetchone()


def update_student_gpa(student_id, new_gpa):
    """Update a student's GPA."""

    conn.execute(
        "UPDATE students SET gpa = ? WHERE id = ?",
        (new_gpa, student_id)
    )

    conn.commit()


def delete_student(student_id):
    """Delete a student."""

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()


def print_students(students):
    """Print student records."""

    for student in students:
        print(
            f"ID: {student['id']} | "
            f"Name: {student['name']} | "
            f"Grade: {student['grade']} | "
            f"GPA: {student['gpa']}"
        )


if __name__ == "__main__":
    create_table()

    # Clear previous test data so rerunning the script
    # does not keep adding duplicate students.
    conn.execute("DELETE FROM students")
    conn.commit()

    # CREATE
    add_student("Alice Johnson", 10, 3.7)
    add_student("Bob Smith", 11, 3.2)
    add_student("Charlie Brown", 12, 3.8)
    add_student("Diana Prince", 10, 3.5)

    # READ
    print("All students:")
    print_students(get_all_students())

    # Read one student
    student = get_student_by_id(2)

    if student:
        print("\nStudent with ID 2:")
        print_students([student])

    # UPDATE
    update_student_gpa(2, 3.6)

    print("\nAfter updating Bob's GPA:")
    print_students(get_all_students())

    # DELETE
    delete_student(3)

    print("\nAfter deleting student ID 3:")
    print_students(get_all_students())

    conn.close()