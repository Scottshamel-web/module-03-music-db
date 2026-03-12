"""
Exercise: Employee Directory Joins
Module 3 — Databases & SQL
Lesson 4 — Practice Exercise
Estimated time: 35 minutes

Objective: Master JOIN types by querying a multi-table employee database.
Understand when to use INNER JOIN vs LEFT JOIN and how NULL reveals missing data.
"""

import sqlite3

# ============================================================
# SETUP
# ============================================================

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE departments (
        id       INTEGER PRIMARY KEY,
        name     TEXT NOT NULL,
        location TEXT
    );
    CREATE TABLE employees (
        id            INTEGER PRIMARY KEY,
        name          TEXT NOT NULL,
        role          TEXT,
        salary        REAL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    CREATE TABLE projects (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,
        employee_id INTEGER,  -- the project lead
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    );
""")

conn.executemany(
    "INSERT INTO departments VALUES (?, ?, ?)",
    [
        (1, "Engineering", "New York"),
        (2, "Marketing",   "Chicago"),
        (3, "HR",          "Remote"),   # <-- no employees → shows in LEFT JOIN demo
    ]
)

conn.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
    [
        (1, "Alice Chen",    "Senior Engineer",  95000, 1),
        (2, "Bob Martinez",  "Engineer",         75000, 1),
        (3, "Carol Davis",   "Lead Engineer",   110000, 1),
        (4, "Dan Wilson",    "Marketing Mgr",    80000, 2),
        (5, "Eva Brown",     "Designer",         70000, 2),
        (6, "Frank Lee",     "HR Manager",       72000, None),  # dept_id NULL → orphan
        (7, "Grace Kim",     "Recruiter",        65000, None),
        (8, "Henry Zhou",    "Analyst",          68000, 1),
    ]
)

conn.executemany(
    "INSERT INTO projects VALUES (?, ?, ?)",
    [
        (1, "API Redesign",        1),   # Alice leads
        (2, "Brand Campaign",      4),   # Dan leads
        (3, "ML Infrastructure",   3),   # Carol leads
        (4, "Hiring Pipeline",     6),   # Frank leads
        # Bob (2), Eva (5), Grace (7), Henry (8) don't lead any project
    ]
)
conn.commit()

print("=" * 60)

# ============================================================
# QUERY 1: INNER JOIN
# Returns only rows where the join condition matches BOTH tables.
# Employees without a department_id are excluded (Frank, Grace).
# ============================================================
print("1. All employees with their department (INNER JOIN):")
print("   (Employees with no department won't appear)")
print("-" * 60)
rows = conn.execute("""
    SELECT e.name, e.role, d.name AS department, d.location
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    ORDER BY d.name, e.name
""").fetchall()
for r in rows:
    print(f"   {r['name']:<15} {r['role']:<20} {r['department']:<12} {r['location']}")

print()

# ============================================================
# QUERY 2: LEFT JOIN (departments → employees)
# Returns ALL rows from the LEFT table (departments), plus matching
# rows from the right. Unmatched right-side columns are NULL.
# HR has no employees, so employee columns show NULL.
# ============================================================
print("2. All departments including those with no employees (LEFT JOIN):")
print("-" * 60)
rows = conn.execute("""
    SELECT d.name AS department, d.location, e.name AS employee
    FROM departments d
    LEFT JOIN employees e ON e.department_id = d.id
    ORDER BY d.name, e.name
""").fetchall()
for r in rows:
    emp = r['employee'] or "(no employees)"
    print(f"   {r['department']:<12} {r['location']:<10} {emp}")

print()

# ============================================================
# QUERY 3: LEFT JOIN (employees → projects)
# Shows all employees, with NULL in project columns for those
# who don't lead any project.
# ============================================================
print("3. All employees and projects they lead (including employees without projects):")
print("-" * 60)
rows = conn.execute("""
    SELECT e.name AS employee, p.title AS project
    FROM employees e
    LEFT JOIN projects p ON p.employee_id = e.id
    ORDER BY e.name
""").fetchall()
for r in rows:
    project = r['project'] or "(no project)"
    print(f"   {r['employee']:<15} {project}")

print()

# ============================================================
# QUERY 4: LEFT JOIN + IS NULL
# The IS NULL filter on the right-side column finds the "unmatched" rows —
# i.e., employees who DON'T lead any project.
# ============================================================
print("4. Employees who don't lead any project (LEFT JOIN + IS NULL):")
print("-" * 60)
rows = conn.execute("""
    SELECT e.name, e.role
    FROM employees e
    LEFT JOIN projects p ON p.employee_id = e.id
    WHERE p.id IS NULL
    ORDER BY e.name
""").fetchall()
for r in rows:
    print(f"   {r['name']:<15} ({r['role']})")

print()

# ============================================================
# QUERY 5: Three-table JOIN
# Chain multiple JOINs to bring in data from a third table.
# Each JOIN adds one more "dimension" of related data.
# ============================================================
print("5. All projects with lead's name AND their department (3-table join):")
print("-" * 60)
rows = conn.execute("""
    SELECT p.title        AS project,
           e.name         AS lead,
           d.name         AS department
    FROM projects p
    JOIN employees   e ON p.employee_id = e.id
    LEFT JOIN departments d ON e.department_id = d.id
    ORDER BY p.title
""").fetchall()
for r in rows:
    dept = r['department'] or "No Department"
    print(f"   {r['project']:<25} Lead: {r['lead']:<15} Dept: {dept}")

conn.close()
