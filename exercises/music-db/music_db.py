import sqlite3


conn = sqlite3.connect("music.db")
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            genre TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            artist_id INTEGER,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        )
    """)

    conn.commit()


def insert_data(conn):
    # Clear old rows so running the script again does not duplicate data
    conn.execute("DELETE FROM albums")
    conn.execute("DELETE FROM artists")

    artists = [
        ("The Weeknd", "R&B"),
        ("Kendrick Lamar", "Hip-Hop"),
        ("Adele", "Pop"),
    ]

    conn.executemany(
        "INSERT INTO artists (name, genre) VALUES (?, ?)",
        artists
    )

    albums = [
        ("After Hours", 2020, 1),
        ("Dawn FM", 2022, 1),
        ("DAMN.", 2017, 2),
        ("Mr. Morale & the Big Steppers", 2022, 2),
        ("21", 2011, 3),
        ("30", 2021, 3),
    ]

    conn.executemany(
        "INSERT INTO albums (title, year, artist_id) VALUES (?, ?, ?)",
        albums
    )

    conn.commit()


def query_albums(conn):
    cursor = conn.execute("""
        SELECT
            albums.title,
            albums.year,
            artists.name
        FROM albums
        JOIN artists
            ON albums.artist_id = artists.id
        ORDER BY artists.name, albums.year
    """)

    return cursor.fetchall()


if __name__ == "__main__":
    create_tables(conn)
    insert_data(conn)

    results = query_albums(conn)

    print("Albums by artist:")

    for row in results:
        print(
            f"{row['title']} ({row['year']}) "
            f"belongs to {row['name']}"
        )

    conn.close()