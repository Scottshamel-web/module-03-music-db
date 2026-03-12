"""
Exercise: The Self-Join
Module 3 | Lesson 4 Stretch | ~25 min

Objective:
  Query hierarchical (self-referential) data using a self-join.
  A self-join treats the same table as two separate tables — one for
  the "child" rows and one for the "parent" rows — and links them by
  the manager_id foreign key.
"""

import sqlite3

# ── Database setup (provided — do not modify) ─────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE employees (
        id         INTEGER PRIMARY KEY,
        name       TEXT    NOT NULL,
        title      TEXT    NOT NULL,
        manager_id INTEGER REFERENCES employees(id)   -- NULL = top of hierarchy
    );

    -- Org chart:
    --   Sarah (CEO)
    --   ├── James (VP Engineering)
    --   │   ├── Alice (Senior Engineer)
    --   │   └── Bob   (Engineer)
    --   └── Maria (VP Marketing)
    --       ├── Carol (Marketing Lead)
    --       └── Dan   (Designer)

    INSERT INTO employees VALUES
      (1, 'Sarah Kim',      'CEO',               NULL),
      (2, 'James Okafor',   'VP Engineering',    1),
      (3, 'Maria Santos',   'VP Marketing',      1),
      (4, 'Alice Chen',     'Senior Engineer',   2),
      (5, 'Bob Williams',   'Engineer',          2),
      (6, 'Carol Davis',    'Marketing Lead',    3),
      (7, 'Dan Petrov',     'Designer',          3);
""")
conn.commit()


# ── Task: Write the self-join query ───────────────────────────────────────────
# A self-join aliases the same table twice:
#   FROM employees AS emp               <- the "child" (subordinate)
#   JOIN employees AS mgr ON emp.manager_id = mgr.id   <- the "manager"
#
# This lets you select columns from both aliases in the same query.

print("Employee — Manager pairs:")
# TODO: write the self-join query
# Use an INNER JOIN to show only employees who HAVE a manager (exclude the CEO).
# SELECT emp.name AS employee, emp.title, mgr.name AS manager
# ...
# ORDER BY mgr.name, emp.name

# query = """
#     SELECT ...
# """
# for row in conn.execute(query):
#     print(f"   {row['employee']:<18} ({row['title']:<20}) reports to {row['manager']}")
print()


# ── Bonus ─────────────────────────────────────────────────────────────────────
# Can you modify your query to also show the CEO (who has no manager)?
# Hint: switch INNER JOIN to LEFT JOIN and handle the NULL manager name.
print("Full org chart (including CEO):")
# TODO: write a LEFT JOIN version so Sarah also appears
# query_bonus = "SELECT ..."
# for row in conn.execute(query_bonus):
#     manager = row['manager'] or "— (top of org)"
#     print(f"   {row['employee']:<18} reports to {manager}")
print()

conn.close()

# Expected output:
# Employee — Manager pairs:
#    Alice Chen         (Senior Engineer    ) reports to James Okafor
#    Bob Williams       (Engineer           ) reports to James Okafor
#    James Okafor       (VP Engineering     ) reports to Sarah Kim
#    Maria Santos       (VP Marketing       ) reports to Sarah Kim
#    Carol Davis        (Marketing Lead     ) reports to Maria Santos
#    Dan Petrov         (Designer           ) reports to Maria Santos
#
# Full org chart (including CEO):
#    Sarah Kim          reports to — (top of org)
#    Alice Chen         reports to James Okafor
#    ...
