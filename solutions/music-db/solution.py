"""
Exercise: Build Your Own Database
Module 3 — Databases & SQL
Lesson 1 — Practice Exercise
Estimated time: 30 minutes

Objective: Create a SQLite database with two related tables, insert data,
and query it using a JOIN. Understand foreign keys and referential integrity.
"""

import sqlite3

# Connect to an in-memory database.
# In real projects you'd use a filename like "music.db" to persist data across runs.
# :memory: is great for learning and testing — clean slate every run, no leftover files.
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Enable foreign key enforcement.
# SQLite does NOT enforce foreign keys by default — you must turn it on per connection.
# This PRAGMA must be run before creating tables or inserting data.
cursor.execute("PRAGMA foreign_keys = ON")

# ============================================================
# CREATE TABLES
# ============================================================

# The artists table is the "parent" — albums will reference it.
cursor.execute("""
    CREATE TABLE artists (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        genre TEXT
    )
""")

# The albums table is the "child" — artist_id is a foreign key.
# REFERENCES artists(id) tells SQLite: artist_id must match an existing artists.id value.
# If you try to insert an album with an artist_id that doesn't exist, SQLite raises an error.
cursor.execute("""
    CREATE TABLE albums (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        title     TEXT NOT NULL,
        year      INTEGER,
        artist_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists(id)
    )
""")

# ============================================================
# INSERT DATA
# ============================================================

# Insert artists first — albums depend on them
artists = [
    ("Taylor Swift", "Pop"),
    ("Kendrick Lamar", "Hip-Hop"),
    ("Radiohead", "Alternative"),
]
cursor.executemany("INSERT INTO artists (name, genre) VALUES (?, ?)", artists)

# Insert albums — note some artists have multiple albums
# We use artist_id values 1, 2, 3 to match the auto-incremented IDs above
albums = [
    ("1989", 2014, 1),          # Taylor Swift
    ("Fearless", 2008, 1),      # Taylor Swift (multiple albums from same artist)
    ("good kid, m.A.A.d city", 2012, 2),  # Kendrick Lamar
    ("DAMN.", 2017, 2),         # Kendrick Lamar
    ("OK Computer", 1997, 3),   # Radiohead
]
cursor.executemany(
    "INSERT INTO albums (title, year, artist_id) VALUES (?, ?, ?)",
    albums
)

conn.commit()

# ============================================================
# QUERY: Albums with Artist Names
# ============================================================

# JOIN combines rows from both tables where the condition matches.
# albums.artist_id = artists.id links each album to its artist.
# Without the JOIN, albums only has artist_id (a number), not the artist's name.
print("All albums with their artist:\n")
cursor.execute("""
    SELECT albums.title, albums.year, artists.name, artists.genre
    FROM albums
    JOIN artists ON albums.artist_id = artists.id
    ORDER BY artists.name, albums.year
""")

rows = cursor.fetchall()
print(f"{'Album':<35} {'Year':<6} {'Artist':<20} {'Genre'}")
print("-" * 75)
for title, year, artist, genre in rows:
    print(f"{title:<35} {year:<6} {artist:<20} {genre}")

# ============================================================
# CLEANUP
# ============================================================
conn.close()
print("\nDatabase connection closed.")
