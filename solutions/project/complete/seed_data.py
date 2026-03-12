"""
seed_data.py — Populate the database with realistic sample data.
Run this script to set up a working library database for manual testing:
    python seed_data.py
Then launch the CLI:
    python cli.py
"""

from library_system import (
    init_db, add_author, add_book, add_borrower, checkout_book
)
from datetime import date


def seed():
    init_db()
    print("Database initialized.")

    # ── Authors ───────────────────────────────────────────────────────────────
    tolkien  = add_author("J.R.R. Tolkien",  "English author, philologist, and academic, best known for The Hobbit and The Lord of the Rings.")
    austen   = add_author("Jane Austen",     "English novelist known for her six major novels including Pride and Prejudice.")
    orwell   = add_author("George Orwell",   "English novelist and essayist, best known for Nineteen Eighty-Four and Animal Farm.")
    le_guin  = add_author("Ursula K. Le Guin", "American author of science fiction and fantasy, known for the Earthsea cycle.")
    gaiman   = add_author("Neil Gaiman",     "English author of fiction for adults and children, known for American Gods and Neverwhere.")
    print(f"Added {5} authors.")

    # ── Books ─────────────────────────────────────────────────────────────────
    add_book("The Hobbit",                  "978-0618260300", tolkien.id,  1937, ["Fantasy", "Adventure", "Children's"])
    add_book("The Fellowship of the Ring",  "978-0618346257", tolkien.id,  1954, ["Fantasy", "Adventure"])
    add_book("The Two Towers",              "978-0618346264", tolkien.id,  1954, ["Fantasy", "Adventure"])
    add_book("The Return of the King",      "978-0618346271", tolkien.id,  1955, ["Fantasy", "Adventure"])
    add_book("Pride and Prejudice",         "978-0141439518", austen.id,   1813, ["Fiction", "Romance", "Classic"])
    add_book("Emma",                        "978-0141439587", austen.id,   1815, ["Fiction", "Romance", "Classic"])
    add_book("Sense and Sensibility",       "978-0141439662", austen.id,   1811, ["Fiction", "Romance", "Classic"])
    add_book("Nineteen Eighty-Four",        "978-0451524935", orwell.id,   1949, ["Fiction", "Dystopia", "Classic"])
    add_book("Animal Farm",                 "978-0451526342", orwell.id,   1945, ["Fiction", "Satire", "Classic"])
    add_book("A Wizard of Earthsea",        "978-0547773742", le_guin.id,  1968, ["Fantasy", "Adventure", "Children's"])
    add_book("The Tombs of Atuan",          "978-0689845369", le_guin.id,  1971, ["Fantasy", "Adventure"])
    add_book("American Gods",               "978-0380789030", gaiman.id,   2001, ["Fantasy", "Mythology"])
    add_book("Neverwhere",                  "978-0060557812", gaiman.id,   1996, ["Fantasy", "Urban Fantasy"])
    add_book("Good Omens",                  "978-0060853976", gaiman.id,   1990, ["Fantasy", "Satire", "Comedy"])
    print(f"Added {14} books.")

    # ── Borrowers ─────────────────────────────────────────────────────────────
    alice   = add_borrower("Alice Chen",       "alice@example.com",   "555-0101")
    bob     = add_borrower("Bob Martinez",     "bob@example.com",     "555-0202")
    carol   = add_borrower("Carol Singh",      "carol@example.com",   "555-0303")
    dan     = add_borrower("Dan Okafor",       "dan@example.com")
    elena   = add_borrower("Elena Petrov",     "elena@example.com",   "555-0505")
    print(f"Added {5} borrowers.")

    # ── Some checkouts (books 1, 5, 8 are now checked out) ───────────────────
    checkout_book(1, alice.id,  days=14)   # The Hobbit
    checkout_book(5, bob.id,    days=21)   # Pride and Prejudice
    checkout_book(8, carol.id,  days=7)    # Nineteen Eighty-Four
    print("Created 3 checkouts.")

    print("\nSeed complete! Launch the CLI with: python cli.py")


if __name__ == "__main__":
    seed()
