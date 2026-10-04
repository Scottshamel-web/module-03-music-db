import sqlite3


# Use an in-memory database for this exercise.
# The database only exists while this script is running.
conn = sqlite3.connect(":memory:")

# This lets us access columns by name, like row["title"].
conn.row_factory = sqlite3.Row

# Turn on foreign key support.
conn.execute("PRAGMA foreign_keys = ON")


def create_tables():
    """Create the members, books, and checkouts tables."""

    conn.execute("""
        CREATE TABLE members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            join_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            year_published INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE checkouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            checkout_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.commit()


def insert_data():
    """Add sample members, books, and checkout records."""

    # Five library members
    members = [
        ("Alice Johnson", "2025-01-10"),
        ("Bob Smith", "2025-02-15"),
        ("Charlie Brown", "2025-03-05"),
        ("Diana Prince", "2025-04-12"),
        ("Eve Williams", "2025-05-20"),
    ]

    conn.executemany(
        """
        INSERT INTO members (name, join_date)
        VALUES (?, ?)
        """,
        members
    )


    # Nine books across several genres.
    # The last book will never be checked out so Query 5 has a result.
    books = [
        ("Python Crash Course", "Technology", 2019),
        ("Clean Code", "Technology", 2008),
        ("AI Engineering", "Technology", 2025),
        ("The Hobbit", "Fantasy", 1937),
        ("The Fellowship of the Ring", "Fantasy", 1954),
        ("1984", "Fiction", 1949),
        ("To Kill a Mockingbird", "Fiction", 1960),
        ("The Martian", "Science Fiction", 2011),
        ("Dune", "Science Fiction", 1965),
    ]

    conn.executemany(
        """
        INSERT INTO books (title, genre, year_published)
        VALUES (?, ?, ?)
        """,
        books
    )


    # There are more than 15 checkouts.
    # Some return dates are NULL because those books have not been returned yet.
    checkouts = [
        (1, 1, "2025-06-01", "2025-06-10"),
        (1, 2, "2025-06-12", "2025-06-20"),
        (1, 4, "2025-07-01", "2025-07-12"),
        (1, 6, "2025-07-20", None),
        (1, 8, "2025-08-01", "2025-08-15"),

        (2, 1, "2025-06-03", "2025-06-11"),
        (2, 3, "2025-06-20", "2025-07-01"),
        (2, 4, "2025-07-15", None),

        (3, 2, "2025-06-05", "2025-06-18"),
        (3, 5, "2025-07-02", "2025-07-14"),
        (3, 6, "2025-08-01", None),

        (4, 1, "2025-06-08", "2025-06-17"),
        (4, 3, "2025-07-04", "2025-07-18"),
        (4, 7, "2025-08-10", None),

        (5, 4, "2025-06-11", "2025-06-22"),
        (5, 5, "2025-07-08", "2025-07-20"),
        (5, 7, "2025-08-12", None),
    ]

    conn.executemany(
        """
        INSERT INTO checkouts
            (member_id, book_id, checkout_date, return_date)
        VALUES (?, ?, ?, ?)
        """,
        checkouts
    )

    conn.commit()


def main():
    create_tables()
    insert_data()

    # ------------------------------------------------------------
    # Query 1
    # Count how many books belong to each genre.
    # GROUP BY creates one result for each genre.
    # ------------------------------------------------------------
    print("\n=== Query 1: Books in Each Genre ===")

    cursor = conn.execute("""
        SELECT genre, COUNT(*) AS book_count
        FROM books
        GROUP BY genre
        ORDER BY genre
    """)

    for row in cursor.fetchall():
        print(f"{row['genre']}: {row['book_count']} books")


    # ------------------------------------------------------------
    # Query 2
    # Count each member's checkouts, sort highest first,
    # and use LIMIT 1 to return the member with the most.
    # ------------------------------------------------------------
    print("\n=== Query 2: Member With the Most Checkouts ===")

    cursor = conn.execute("""
        SELECT
            members.name,
            COUNT(checkouts.id) AS checkout_count
        FROM members
        JOIN checkouts
            ON members.id = checkouts.member_id
        GROUP BY members.id, members.name
        ORDER BY checkout_count DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    print(
        f"{row['name']} - "
        f"{row['checkout_count']} checkouts"
    )


    # ------------------------------------------------------------
    # Query 3
    # First, the subquery counts checkouts for each member.
    # The outer query then finds the average of those counts.
    # ------------------------------------------------------------
    print("\n=== Query 3: Average Checkouts Per Member ===")

    cursor = conn.execute("""
        SELECT AVG(checkout_count) AS average_checkouts
        FROM (
            SELECT
                members.id,
                COUNT(checkouts.id) AS checkout_count
            FROM members
            LEFT JOIN checkouts
                ON members.id = checkouts.member_id
            GROUP BY members.id
        )
    """)

    row = cursor.fetchone()

    print(
        f"Average checkouts per member: "
        f"{row['average_checkouts']:.2f}"
    )


    # ------------------------------------------------------------
    # Query 4
    # Count checkouts by genre.
    # HAVING filters the grouped results after GROUP BY.
    # ------------------------------------------------------------
    print("\n=== Query 4: Genres With More Than 3 Checkouts ===")

    cursor = conn.execute("""
        SELECT
            books.genre,
            COUNT(checkouts.id) AS checkout_count
        FROM books
        JOIN checkouts
            ON books.id = checkouts.book_id
        GROUP BY books.genre
        HAVING COUNT(checkouts.id) > 3
        ORDER BY checkout_count DESC
    """)

    for row in cursor.fetchall():
        print(
            f"{row['genre']}: "
            f"{row['checkout_count']} checkouts"
        )


    # ------------------------------------------------------------
    # Query 5
    # The subquery gets every book ID that appears in checkouts.
    # NOT IN leaves us with books that were never checked out.
    # ------------------------------------------------------------
    print("\n=== Query 5: Books Never Checked Out ===")

    cursor = conn.execute("""
        SELECT title, genre, year_published
        FROM books
        WHERE id NOT IN (
            SELECT book_id
            FROM checkouts
        )
        ORDER BY title
    """)

    for row in cursor.fetchall():
        print(
            f"{row['title']} | "
            f"{row['genre']} | "
            f"{row['year_published']}"
        )


    # Close the database when we're finished.
    conn.close()


if __name__ == "__main__":
    main()