import sqlite3


# Using an in-memory database for this exercise.
# It only exists while the program is running.
conn = sqlite3.connect(":memory:")

# This lets me access columns by name instead of position.
conn.row_factory = sqlite3.Row

# Turn on foreign key support.
conn.execute("PRAGMA foreign_keys = ON")


def create_tables():
    """Create the three tables used in this exercise."""

    # Departments table
    conn.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    # Employees table
    # department_id connects each employee to a department.
    conn.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

    # Projects table
    # employee_id represents the employee leading the project.
    conn.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)


def insert_sample_data():
    """Add sample departments, employees, and projects."""

    # I added a fourth department with no employees
    # so the LEFT JOIN can show that case.
    departments = [
        (1, "Engineering", "New York"),
        (2, "Sales", "Chicago"),
        (3, "Human Resources", "Boston"),
        (4, "Marketing", "Los Angeles")
    ]

    # Engineering has more than 3 employees,
    # which meets one of the assignment requirements.
    employees = [
        (1, "Alice Johnson", "Software Engineer", 95000, 1),
        (2, "Bob Smith", "Senior Engineer", 115000, 1),
        (3, "Charlie Brown", "Data Analyst", 85000, 1),
        (4, "Diana Prince", "Sales Manager", 90000, 2),
        (5, "Eve Williams", "Sales Representative", 65000, 2),
        (6, "Frank Miller", "HR Manager", 82000, 3),
        (7, "Grace Lee", "Recruiter", 70000, 3),
        (8, "Henry Davis", "DevOps Engineer", 100000, 1)
    ]

    # Some employees lead projects and some do not.
    projects = [
        (1, "Website Redesign", 1),
        (2, "Cloud Migration", 2),
        (3, "Sales Dashboard", 4),
        (4, "Hiring Initiative", 6),
        (5, "Data Cleanup", 3)
    ]

    conn.executemany(
        "INSERT INTO departments VALUES (?, ?, ?)",
        departments
    )

    conn.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
        employees
    )

    conn.executemany(
        "INSERT INTO projects VALUES (?, ?, ?)",
        projects
    )

    conn.commit()


def query_1():
    """Show every employee with their department name."""

    print("\n=== Query 1: Employees with Departments ===")

    # INNER JOIN only returns rows where there is a match
    # between employees and departments.
    query = """
        SELECT
            employees.name AS employee,
            employees.role,
            departments.name AS department
        FROM employees
        INNER JOIN departments
            ON employees.department_id = departments.id
        ORDER BY employees.id
    """

    rows = conn.execute(query).fetchall()

    for row in rows:
        print(
            f"{row['employee']:<18} "
            f"{row['role']:<22} "
            f"{row['department']}"
        )


def query_2():
    """Show all departments, even if they have no employees."""

    print("\n=== Query 2: All Departments ===")

    # LEFT JOIN keeps every department.
    # If no employee matches, the employee value will be NULL.
    query = """
        SELECT
            departments.name AS department,
            departments.location,
            employees.name AS employee
        FROM departments
        LEFT JOIN employees
            ON departments.id = employees.department_id
        ORDER BY departments.id
    """

    rows = conn.execute(query).fetchall()

    for row in rows:
        employee = row["employee"]

        # Make NULL easier to read in the output.
        if employee is None:
            employee = "No employees"

        print(
            f"{row['department']:<18} "
            f"{row['location']:<15} "
            f"{employee}"
        )


def query_3():
    """Show all employees and any projects they lead."""

    print("\n=== Query 3: Employees and Projects ===")

    # LEFT JOIN is used here because I still want employees
    # to appear even if they are not leading a project.
    query = """
        SELECT
            employees.name AS employee,
            projects.title AS project
        FROM employees
        LEFT JOIN projects
            ON employees.id = projects.employee_id
        ORDER BY employees.id
    """

    rows = conn.execute(query).fetchall()

    for row in rows:
        project = row["project"]

        if project is None:
            project = "No project"

        print(f"{row['employee']:<18} {project}")


def query_4():
    """Find employees who are not leading any project."""

    print("\n=== Query 4: Employees Without Projects ===")

    # The LEFT JOIN keeps every employee.
    # Then IS NULL filters it down to only employees
    # who had no matching project.
    query = """
        SELECT
            employees.name AS employee,
            employees.role
        FROM employees
        LEFT JOIN projects
            ON employees.id = projects.employee_id
        WHERE projects.id IS NULL
        ORDER BY employees.id
    """

    rows = conn.execute(query).fetchall()

    for row in rows:
        print(f"{row['employee']:<18} {row['role']}")


def query_5():
    """Show each project with the lead and their department."""

    print("\n=== Query 5: Projects, Leads, and Departments ===")

    # This query joins all three tables.
    # projects connects to employees,
    # then employees connects to departments.
    query = """
        SELECT
            projects.title AS project,
            employees.name AS lead,
            departments.name AS department
        FROM projects
        INNER JOIN employees
            ON projects.employee_id = employees.id
        INNER JOIN departments
            ON employees.department_id = departments.id
        ORDER BY projects.id
    """

    rows = conn.execute(query).fetchall()

    for row in rows:
        print(
            f"{row['project']:<20} "
            f"{row['lead']:<18} "
            f"{row['department']}"
        )


def main():
    # Set everything up first.
    create_tables()
    insert_sample_data()

    # Run each required query.
    query_1()
    query_2()
    query_3()
    query_4()
    query_5()

    # Close the database connection when finished.
    conn.close()


if __name__ == "__main__":
    main()