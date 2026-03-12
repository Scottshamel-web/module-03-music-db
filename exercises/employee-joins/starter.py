"""
Exercise: Employee Directory Joins
Module 3 | Lesson 4 | ~35 min

Objective:
  Write INNER JOIN and LEFT JOIN queries across three related tables to
  answer real-world HR questions. Understanding the difference between
  INNER JOIN (only matching rows) and LEFT JOIN (all left rows, NULLs
  for non-matches) is a critical SQL skill.
"""

import sqlite3

# ── Database setup (provided — do not modify) ─────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

conn.executescript("""
    CREATE TABLE departments (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );

    CREATE TABLE employees (
        id            INTEGER PRIMARY KEY,
        name          TEXT NOT NULL,
        email         TEXT,
        salary        REAL,
        department_id INTEGER REFERENCES departments(id)
    );

    CREATE TABLE projects (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,
        employee_id INTEGER REFERENCES employees(id)
    );

    INSERT INTO departments VALUES
      (1, 'Engineering', 'San Francisco'),
      (2, 'Marketing',   'New York'),
      (3, 'Design',      'Austin'),
      (4, 'Legal',       'Chicago');   -- no employees assigned yet

    INSERT INTO employees VALUES
      (1, 'Alice Chen',    'alice@co.com',   115000, 1),
      (2, 'Bob Martinez',  'bob@co.com',      85000, 2),
      (3, 'Carol Singh',   'carol@co.com',    98000, 1),
      (4, 'Dan Okafor',    'dan@co.com',      72000, 3),
      (5, 'Elena Petrov',  'elena@co.com',   105000, 1),
      (6, 'Frank Nguyen',  'frank@co.com',    91000, NULL);  -- not in any department

    INSERT INTO projects VALUES
      (1, 'API Redesign',        1),
      (2, 'Brand Campaign',      2),
      (3, 'Cloud Migration',     3),
      (4, 'UI Style Guide',      4),
      (5, 'Security Audit',      1),
      (6, 'Social Media Launch', 2);
    -- Note: employee 5 (Elena) and 6 (Frank) have no projects yet.
""")
conn.commit()


# ── Query 1: INNER JOIN — employees with their department ─────────────────────
# INNER JOIN returns only rows where a match exists in BOTH tables.
# Employees without a department (Frank) will NOT appear.
print("1. All employees with their department and city:")
# TODO: write an INNER JOIN between employees and departments
# query1 = """
#     SELECT ...
#     FROM employees
#     INNER JOIN departments ON ...
#     ORDER BY departments.name, employees.name
# """
# for row in conn.execute(query1):
#     print(f"   {row['name']} — {row['dept_name']} ({row['city']})")
print()

# ── Query 2: LEFT JOIN — all employees, even those without a department ────────
# LEFT JOIN returns ALL rows from the left table (employees), filling in
# NULL for department columns when no match exists.
print("2. All employees (including those not in a department):")
# TODO: write a LEFT JOIN between employees and departments
# query2 = """
#     SELECT ...
#     FROM employees
#     LEFT JOIN departments ON ...
#     ORDER BY employees.name
# """
# for row in conn.execute(query2):
#     dept = row['dept_name'] or "No department"
#     print(f"   {row['name']} — {dept}")
print()

# ── Query 3: INNER JOIN — employees with their projects ───────────────────────
print("3. Employees and their assigned projects:")
# TODO: write an INNER JOIN between employees and projects
# Only employees who have at least one project should appear.
# query3 = "SELECT ..."
# for row in conn.execute(query3):
#     print(f"   {row['employee_name']} → {row['project_title']}")
print()

# ── Query 4: LEFT JOIN — all employees, showing project or "No project" ────────
print("4. All employees and their project (or 'No project assigned'):")
# TODO: write a LEFT JOIN between employees and projects
# query4 = "SELECT ..."
# for row in conn.execute(query4):
#     project = row['project_title'] or "No project assigned"
#     print(f"   {row['employee_name']} → {project}")
print()

# ── Query 5: Three-table JOIN — employees, departments, and projects ───────────
print("5. Full directory: employee, department, project:")
# TODO: JOIN all three tables (employees + departments + projects)
# Use LEFT JOINs so employees with no department or no project still appear.
# query5 = "SELECT ..."
# for row in conn.execute(query5):
#     dept    = row['dept_name']    or "—"
#     project = row['project_title'] or "—"
#     print(f"   {row['employee_name']:<16} | {dept:<15} | {project}")
print()

conn.close()

# Expected output (sample):
# 1. All employees with their department and city:
#    Alice Chen — Engineering (San Francisco)
#    Carol Singh — Engineering (San Francisco)
#    Elena Petrov — Engineering (San Francisco)
#    Bob Martinez — Marketing (New York)
#    Frank Nguyen — <not shown — no department>
#    ...
#
# 2. All employees (including those not in a department):
#    Alice Chen — Engineering
#    Bob Martinez — Marketing
#    ...
#    Frank Nguyen — No department
#
# 5. Full directory: employee, department, project:
#    Alice Chen       | Engineering     | API Redesign
#    Alice Chen       | Engineering     | Security Audit
#    Bob Martinez     | Marketing       | Brand Campaign
#    ...
