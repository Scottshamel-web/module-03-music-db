"""
Exercise: Library Analytics
Module 3 | Lesson 5 | ~35 min

Objective:
  Write analytical SQL queries using GROUP BY, HAVING, aggregate functions
  (COUNT, AVG), and subqueries. These tools turn raw rows into insights.

Key concepts:
  - GROUP BY collapses many rows into one row per group.
  - Aggregate functions (COUNT, AVG, MAX, SUM) compute values across the group.
  - HAVING filters AFTER grouping (WHERE filters BEFORE grouping).
  - Subqueries let you use the result of one SELECT inside another.
"""

import sqlite3

# ── Database setup (provided — do not modify) ─────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE members (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        tier TEXT NOT NULL DEFAULT 'standard'  -- 'standard' or 'premium'
    );

    CREATE TABLE books (
        id     INTEGER PRIMARY KEY,
        title  TEXT NOT NULL,
        genre  TEXT NOT NULL,
        pages  INTEGER
    );

    CREATE TABLE checkouts (
        id          INTEGER PRIMARY KEY,
        member_id   INTEGER REFERENCES members(id),
        book_id     INTEGER REFERENCES books(id),
        checkout_date TEXT NOT NULL,       -- stored as 'YYYY-MM-DD' strings
        return_date   TEXT                 -- NULL if not returned
    );

    INSERT INTO members VALUES
      (1, 'Alice Chen',    'premium'),
      (2, 'Bob Martinez',  'standard'),
      (3, 'Carol Singh',   'premium'),
      (4, 'Dan Okafor',    'standard'),
      (5, 'Elena Petrov',  'premium');

    INSERT INTO books VALUES
      (1,  'The Hobbit',               'Fantasy',  310),
      (2,  'Dune',                     'Sci-Fi',   688),
      (3,  'Pride and Prejudice',      'Classic',  432),
      (4,  'Neuromancer',              'Sci-Fi',   271),
      (5,  'Good Omens',               'Fantasy',  413),
      (6,  'Nineteen Eighty-Four',     'Classic',  328),
      (7,  'The Left Hand of Darkness','Sci-Fi',   286),
      (8,  'Jane Eyre',                'Classic',  507),
      (9,  'American Gods',            'Fantasy',  635),
      (10, 'Foundation',               'Sci-Fi',   244);

    INSERT INTO checkouts VALUES
      (1,  1, 1,  '2024-01-05', '2024-01-19'),
      (2,  1, 2,  '2024-01-20', '2024-02-03'),
      (3,  1, 5,  '2024-02-10', '2024-02-24'),
      (4,  2, 3,  '2024-01-08', '2024-01-22'),
      (5,  2, 6,  '2024-02-01', NULL),
      (6,  3, 2,  '2024-01-15', '2024-01-29'),
      (7,  3, 4,  '2024-02-05', '2024-02-19'),
      (8,  3, 7,  '2024-03-01', NULL),
      (9,  4, 10, '2024-01-20', '2024-02-03'),
      (10, 5, 1,  '2024-02-01', '2024-02-15'),
      (11, 5, 9,  '2024-02-20', NULL),
      (12, 1, 8,  '2024-03-05', NULL);
""")
conn.commit()


# ── Query 1: Checkout count per member ────────────────────────────────────────
# GROUP BY collapses all checkout rows for a member into a single summary row.
print("1. Number of checkouts per member (most active first):")
# TODO: write a query that JOINs members to checkouts, groups by member,
#       and COUNTs how many checkouts each has.
# query1 = """
#     SELECT members.name, COUNT(checkouts.id) AS checkout_count
#     FROM ...
#     GROUP BY ...
#     ORDER BY checkout_count DESC
# """
# for row in conn.execute(query1):
#     print(f"   {row['name']}: {row['checkout_count']} checkouts")
print()

# ── Query 2: Most popular genre ───────────────────────────────────────────────
# JOIN books to checkouts, group by genre, count how many times each genre
# was checked out.
print("2. Most popular genres by checkout count:")
# TODO: write the query
# query2 = "SELECT ..."
# for row in conn.execute(query2):
#     print(f"   {row['genre']}: {row['count']} checkouts")
print()

# ── Query 3: Members with more than 2 checkouts (HAVING) ─────────────────────
# HAVING is like WHERE, but it filters on aggregated values AFTER grouping.
# WHERE cannot reference COUNT() — HAVING can.
print("3. Members with more than 2 checkouts:")
# TODO: write the query using GROUP BY + HAVING COUNT(...) > 2
# query3 = "SELECT ..."
# for row in conn.execute(query3):
#     print(f"   {row['name']}: {row['checkout_count']} checkouts")
print()

# ── Query 4: Average pages per genre ─────────────────────────────────────────
print("4. Average book length (pages) per genre:")
# TODO: write a query grouping books by genre and using AVG(pages)
# query4 = "SELECT ..."
# for row in conn.execute(query4):
#     print(f"   {row['genre']}: {row['avg_pages']:.0f} avg pages")
print()

# ── Query 5: Subquery — members who have checked out more than the average ────
# A subquery computes the average checkout count first, then the outer query
# filters members against that value.
print("5. Members with above-average checkout counts:")
# TODO: write a query using a subquery in the HAVING or WHERE clause
# Hint structure:
#   SELECT name, COUNT(...) AS cnt FROM ...
#   GROUP BY member_id
#   HAVING cnt > (SELECT AVG(cnt) FROM (SELECT COUNT(...) AS cnt FROM checkouts GROUP BY member_id))
# query5 = "SELECT ..."
# for row in conn.execute(query5):
#     print(f"   {row['name']}: {row['checkout_count']} checkouts")
print()

conn.close()

# Expected output (sample):
# 1. Number of checkouts per member (most active first):
#    Alice Chen: 4 checkouts
#    Carol Singh: 3 checkouts
#    Elena Petrov: 2 checkouts
#    Bob Martinez: 2 checkouts
#    Dan Okafor: 1 checkouts
#
# 2. Most popular genres by checkout count:
#    Fantasy: 5 checkouts
#    Sci-Fi: 4 checkouts
#    Classic: 3 checkouts
#
# 3. Members with more than 2 checkouts:
#    Alice Chen: 4 checkouts
#    Carol Singh: 3 checkouts
