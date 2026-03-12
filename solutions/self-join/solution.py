"""
Exercise: The Self-Join
Module 3 — Databases & SQL
Lesson 4 — Stretch Challenge
Estimated time: 25 minutes

Objective: Use a self-join to query hierarchical data within a single table.

When self-joins are useful:
- Org charts (employee.manager_id → employee.id)
- Category trees (category.parent_id → category.id)
- Friend relationships (friendship where both user_a and user_b are in the same table)
- Comparing rows within the same table (find duplicate emails, find price changes)

The key technique: give the same table two aliases so SQL can treat it as two
separate sources. e1 = "the employee", e2 = "the employee's manager".
"""

import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.execute("""
    CREATE TABLE employees (
        id         INTEGER PRIMARY KEY,
        name       TEXT NOT NULL,
        role       TEXT,
        manager_id INTEGER,  -- NULL for the top of the hierarchy (CEO)
        FOREIGN KEY (manager_id) REFERENCES employees(id)
    )
""")

# Build a hierarchy: CEO → 2 VPs → 3 managers → 3 ICs
# Note: manager_id must reference an id that already exists, so insert top-down
conn.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    [
        # id, name, role, manager_id
        (1, "Sandra Lee",    "CEO",               None),  # top of hierarchy
        (2, "James Park",    "VP Engineering",    1),     # reports to CEO
        (3, "Maria Torres",  "VP Operations",     1),     # reports to CEO
        (4, "Alex Kim",      "Eng Manager",       2),     # reports to VP Eng
        (5, "Priya Nair",    "Ops Manager",       3),     # reports to VP Ops
        (6, "Tom Chen",      "Eng Manager",       2),     # reports to VP Eng
        (7, "Zoe Adams",     "Software Engineer", 4),     # reports to Eng Manager
        (8, "Raj Patel",     "Software Engineer", 4),     # reports to Eng Manager
        (9, "Nina Brown",    "Operations Lead",   5),     # reports to Ops Manager
    ]
)
conn.commit()

# ============================================================
# SELF-JOIN QUERY
# We alias the employees table twice:
#   e1 = the employee we're describing
#   e2 = that employee's manager (also in the employees table)
# LEFT JOIN so the CEO (manager_id IS NULL) still appears with NULL manager name.
# ============================================================
print("Employee Hierarchy (self-join):\n")
print(f"{'Employee':<22} {'Role':<22} {'Manager'}")
print("-" * 60)

rows = conn.execute("""
    SELECT
        e1.name       AS employee,
        e1.role       AS role,
        e2.name       AS manager
    FROM employees e1
    LEFT JOIN employees e2 ON e1.manager_id = e2.id
    ORDER BY e1.manager_id NULLS FIRST, e1.id
""").fetchall()

for r in rows:
    manager = r['manager'] or "(top of hierarchy)"
    print(f"{r['employee']:<22} {r['role']:<22} {manager}")

conn.close()
