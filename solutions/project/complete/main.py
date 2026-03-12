"""
Module 3 Project: Library Management System
main.py — Non-interactive scripted demo

Runs without any user input to demonstrate all system functionality:
  1. Initializes the in-memory database
  2. Adds authors, books, and borrowers
  3. Checks out books and returns one
  4. Queries: search by author, overdue books, popular genres, available books
"""

from library_system import (
    init_db,
    add_author, add_book, add_borrower,
    checkout_book, return_book,
    find_books_by_author, get_overdue_books,
    get_popular_genres, get_available_books,
)
from datetime import date, timedelta


def main():
    # ── 1. Initialize the database ────────────────────────────────────────────
    init_db()
    print("Database initialized.\n")

    # ── 2. Add authors ────────────────────────────────────────────────────────
    tolkien  = add_author("J.R.R. Tolkien",  "Author of The Lord of the Rings trilogy.")
    austen   = add_author("Jane Austen",     "English novelist known for her social commentary.")
    orwell   = add_author("George Orwell",   "English novelist and essayist.")
    print(f"Added authors: {tolkien.name}, {austen.name}, {orwell.name}")

    # ── 3. Add books ──────────────────────────────────────────────────────────
    hobbit   = add_book("The Hobbit",              "978-0618260300", tolkien.id,  1937, ["Fantasy", "Adventure"])
    lotr     = add_book("The Fellowship of the Ring", "978-0618346257", tolkien.id, 1954, ["Fantasy", "Adventure"])
    two_towers = add_book("The Two Towers",        "978-0618346264", tolkien.id,  1954, ["Fantasy", "Adventure"])
    pride    = add_book("Pride and Prejudice",     "978-0141439518", austen.id,   1813, ["Fiction", "Romance"])
    emma     = add_book("Emma",                    "978-0141439587", austen.id,   1815, ["Fiction", "Romance"])
    sense    = add_book("Sense and Sensibility",   "978-0141439662", austen.id,   1811, ["Fiction", "Romance"])
    n1984    = add_book("Nineteen Eighty-Four",    "978-0451524935", orwell.id,   1949, ["Fiction", "Dystopia"])
    farm     = add_book("Animal Farm",             "978-0451526342", orwell.id,   1945, ["Fiction", "Dystopia", "Satire"])
    print(f"Added {8} books.\n")

    # ── 4. Add borrowers ──────────────────────────────────────────────────────
    alice   = add_borrower("Alice Chen",    "alice@example.com",   "555-0101")
    bob     = add_borrower("Bob Martinez",  "bob@example.com",     "555-0202")
    carol   = add_borrower("Carol Singh",   "carol@example.com")
    dan     = add_borrower("Dan Okafor",    "dan@example.com",     "555-0404")
    print(f"Added borrowers: {alice.name}, {bob.name}, {carol.name}, {dan.name}\n")

    # ── 5. Check out 3 books ──────────────────────────────────────────────────
    co1 = checkout_book(hobbit.id,  alice.id, days=14)
    co2 = checkout_book(n1984.id,   bob.id,   days=7)
    co3 = checkout_book(pride.id,   carol.id, days=14)
    print("Checked out:")
    print(f"  [{co1.id}] '{hobbit.title}' -> {alice.name}  (due {co1.due_date})")
    print(f"  [{co2.id}] '{n1984.title}' -> {bob.name}  (due {co2.due_date})")
    print(f"  [{co3.id}] '{pride.title}' -> {carol.name}  (due {co3.due_date})\n")

    # ── 6. Return one book ────────────────────────────────────────────────────
    co1_returned = return_book(co1.id)
    print(f"Returned: checkout #{co1_returned.id} on {co1_returned.return_date}\n")

    # ── 7. Query: find books by author ────────────────────────────────────────
    print("=== Books by 'Tolkien' ===")
    for book in find_books_by_author("Tolkien"):
        status = "available" if book.available else "checked out"
        print(f"  - {book.title} ({book.published_year}) [{status}]")
    print()

    # ── 8. Query: overdue books ───────────────────────────────────────────────
    # Simulate an overdue situation by checking what is outstanding
    # (In a live system these would be past-due; here we just show the active checkouts)
    print("=== Currently Checked Out (not yet returned) ===")
    overdue = get_overdue_books()
    if overdue:
        for co in overdue:
            print(f"  - Checkout #{co.id}: book_id={co.book_id}, due={co.due_date}")
    else:
        print("  No overdue books (all due dates are in the future for this demo).")
    print()

    # ── 9. Query: popular genres ──────────────────────────────────────────────
    print("=== Top 3 Genres by Checkout Count ===")
    for genre_name, count in get_popular_genres(limit=3):
        print(f"  {genre_name}: {count} checkout(s)")
    print()

    # ── 10. Query: available books ────────────────────────────────────────────
    print("=== Available Books ===")
    for book in get_available_books():
        print(f"  [{book.id}] {book.title} — {book.author.name}")
    print()

    print("Demo complete.")


if __name__ == "__main__":
    main()
