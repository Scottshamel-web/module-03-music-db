"""
Exercise: Library Analytics
Module 3 — Databases & SQL
Lesson 5 — Practice Exercise
Estimated time: 35 minutes

Objective: Write analytical SQL queries using GROUP BY, HAVING, aggregation
functions (COUNT, AVG), and subqueries to answer real business questions.
"""

import sqlite3

# ============================================================
# SETUP
# ============================================================

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE members (
        id        INTEGER PRIMARY KEY,
        name      TEXT NOT NULL,
        join_date TEXT
    );
    CREATE TABLE books (
        id             INTEGER PRIMARY KEY,
        title          TEXT NOT NULL,
        genre          TEXT,
        year_published INTEGER
    );
    CREATE TABLE checkouts (
        id            INTEGER PRIMARY KEY,
        member_id     INTEGER,
        book_id       INTEGER,
        checkout_date TEXT,
        return_date   TEXT,   -- NULL if not yet returned
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (book_id)   REFERENCES books(id)
    );
""")

conn.executemany("INSERT INTO members VALUES (?, ?, ?)", [
    (1, "Alice Chen",   "2022-01-15"),
    (2, "Bob Martinez", "2022-03-20"),
    (3, "Carol Davis",  "2023-06-01"),
    (4, "Dan Wilson",   "2023-09-10"),
    (5, "Eva Brown",    "2024-01-05"),
])

conn.executemany("INSERT INTO books VALUES (?, ?, ?, ?)", [
    (1,  "Dune",                    "Science Fiction", 1965),
    (2,  "The Great Gatsby",        "Fiction",         1925),
    (3,  "Sapiens",                 "Non-Fiction",     2011),
    (4,  "The Girl with the Dragon Tattoo", "Mystery", 2005),
    (5,  "Educated",                "Non-Fiction",     2018),
    (6,  "Foundation",              "Science Fiction", 1951),
    (7,  "Gone Girl",               "Mystery",         2012),
    (8,  "Thinking, Fast and Slow", "Non-Fiction",     2011),
    (9,  "Project Hail Mary",       "Science Fiction", 2021),
    (10, "The Silent Patient",      "Mystery",         2019),  # never checked out
])

conn.executemany("INSERT INTO checkouts VALUES (?, ?, ?, ?, ?)", [
    (1,  1, 1, "2024-01-10", "2024-01-24"),  # Alice checked out Dune
    (2,  1, 3, "2024-02-01", "2024-02-15"),  # Alice checked out Sapiens
    (3,  1, 6, "2024-03-05", None),           # Alice has Foundation (not returned)
    (4,  2, 2, "2024-01-15", "2024-01-29"),  # Bob checked out Great Gatsby
    (5,  2, 4, "2024-02-10", "2024-02-24"),  # Bob checked out Dragon Tattoo
    (6,  2, 7, "2024-03-01", "2024-03-15"),  # Bob checked out Gone Girl
    (7,  2, 9, "2024-04-01", None),           # Bob has Project Hail Mary
    (8,  3, 1, "2024-02-20", "2024-03-05"),  # Carol checked out Dune
    (9,  3, 5, "2024-03-10", None),           # Carol has Educated
    (10, 4, 8, "2024-01-20", "2024-02-03"),  # Dan checked out Thinking Fast and Slow
    (11, 4, 3, "2024-04-05", None),           # Dan has Sapiens
    (12, 5, 2, "2024-03-15", "2024-03-29"),  # Eva checked out Great Gatsby
    (13, 5, 6, "2024-04-10", None),           # Eva has Foundation
    (14, 1, 9, "2024-05-01", None),           # Alice has Project Hail Mary (2nd checkout)
    (15, 2, 8, "2024-05-10", None),           # Bob has Thinking Fast and Slow
])
conn.commit()

# ============================================================
# QUERY 1: Books per genre
# GROUP BY collapses all rows with the same genre into one row,
# then COUNT(*) counts how many rows were in each group.
# ============================================================
print("1. Books per genre:")
print("-" * 40)
rows = conn.execute("""
    SELECT genre, COUNT(*) AS book_count
    FROM books
    GROUP BY genre
    ORDER BY book_count DESC
""").fetchall()
for r in rows:
    print(f"   {r['genre']:<20} {r['book_count']} books")

print()

# ============================================================
# QUERY 2: Member with most checkouts
# GROUP BY member_id, then ORDER BY count DESC, LIMIT 1 = top result
# ============================================================
print("2. Member with most checkouts:")
print("-" * 40)
row = conn.execute("""
    SELECT m.name, COUNT(*) AS checkout_count
    FROM checkouts c
    JOIN members m ON c.member_id = m.id
    GROUP BY c.member_id
    ORDER BY checkout_count DESC
    LIMIT 1
""").fetchone()
print(f"   {row['name']} with {row['checkout_count']} checkouts")

print()

# ============================================================
# QUERY 3: Average checkouts per member
# Total checkouts ÷ total members. Use a subquery for clarity.
# ============================================================
print("3. Average checkouts per member:")
print("-" * 40)
row = conn.execute("""
    SELECT ROUND(AVG(checkout_count), 2) AS avg_checkouts
    FROM (
        SELECT member_id, COUNT(*) AS checkout_count
        FROM checkouts
        GROUP BY member_id
    )
""").fetchone()
print(f"   {row['avg_checkouts']} checkouts per member on average")

print()

# ============================================================
# QUERY 4: HAVING filters AFTER grouping (WHERE filters BEFORE)
# WHERE genre = 'X' would filter rows before counting.
# HAVING count > 2 filters the already-computed groups.
# Rule of thumb: if your condition uses an aggregate (COUNT, SUM, AVG), use HAVING.
# ============================================================
print("4. Genres with more than 2 checkouts:")
print("-" * 40)
rows = conn.execute("""
    SELECT b.genre, COUNT(*) AS checkout_count
    FROM checkouts c
    JOIN books b ON c.book_id = b.id
    GROUP BY b.genre
    HAVING checkout_count > 2
    ORDER BY checkout_count DESC
""").fetchall()
for r in rows:
    print(f"   {r['genre']:<20} {r['checkout_count']} checkouts")

print()

# ============================================================
# QUERY 5: Books never checked out (subquery with NOT IN)
# The subquery finds all book_ids that HAVE been checked out.
# NOT IN filters to only books whose id isn't in that set.
# Alternative: LEFT JOIN books ON checkouts.book_id = books.id WHERE checkouts.id IS NULL
# ============================================================
print("5. Books never checked out:")
print("-" * 40)
rows = conn.execute("""
    SELECT title, genre, year_published
    FROM books
    WHERE id NOT IN (
        SELECT DISTINCT book_id FROM checkouts
    )
""").fetchall()
for r in rows:
    print(f"   {r['title']} ({r['genre']}, {r['year_published']})")

conn.close()
