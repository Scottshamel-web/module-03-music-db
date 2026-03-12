"""
Exercise: Contact Manager
Module 3 | Lesson 7 | ~35 min

Objective:
  Build a CRUD contact manager using SQLAlchemy Sessions. Practice
  adding, querying, updating, and deleting ORM objects within session
  context managers.
"""

from sqlalchemy import create_engine, String, Boolean, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── Contact model (provided — do not modify) ──────────────────────────────────
class Contact(Base):
    __tablename__ = "contacts"

    id:       Mapped[int]           = mapped_column(Integer, primary_key=True)
    name:     Mapped[str]           = mapped_column(String, nullable=False)
    email:    Mapped[str]           = mapped_column(String, unique=True, nullable=False)
    phone:    Mapped[Optional[str]] = mapped_column(String, nullable=True)
    favorite: Mapped[bool]          = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        fav = " [fav]" if self.favorite else ""
        return f"<Contact {self.name} <{self.email}>{fav}>"


# Create tables
Base.metadata.create_all(engine)


# ── Functions — implement each one ────────────────────────────────────────────

def add_contact(name: str, email: str, phone: str = None) -> Contact:
    """
    Insert a new contact. Returns the created Contact object.
    Raises ValueError if a contact with that email already exists.
    """
    # TODO: open a Session
    # TODO: check if a contact with the same email already exists; raise ValueError if so
    # TODO: create and add the Contact, commit, refresh, return it
    pass


def list_contacts() -> list:
    """Return all contacts ordered by name."""
    # TODO: use select(Contact).order_by(Contact.name)
    pass


def find_contact(email: str) -> Contact:
    """
    Return the Contact with the given email, or None if not found.
    """
    # TODO: use select(Contact).where(Contact.email == email)
    pass


def update_phone(email: str, new_phone: str) -> bool:
    """
    Update the phone number for the contact with the given email.
    Returns True if found and updated, False if not found.
    """
    # TODO: find the contact, update phone, commit
    pass


def toggle_favorite(email: str) -> bool:
    """
    Flip the favorite flag for the contact with the given email.
    Returns the new value of favorite, or raises ValueError if not found.
    """
    # TODO: find the contact, flip contact.favorite, commit, return new value
    pass


def delete_contact(email: str) -> bool:
    """
    Delete the contact with the given email.
    Returns True if deleted, False if not found.
    """
    # TODO: find the contact, session.delete(), commit
    pass


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Add contacts
    print("Adding contacts...")
    c1 = add_contact("Alice Chen",   "alice@example.com",  "555-0101")
    c2 = add_contact("Bob Martinez", "bob@example.com")
    c3 = add_contact("Carol Singh",  "carol@example.com",  "555-0303")
    print(f"  Created: {c1}, {c2}, {c3}")

    # List all
    print("\nAll contacts:")
    for c in list_contacts():
        print(f"  {c}")

    # Find by email
    print("\nFind alice@example.com:")
    found = find_contact("alice@example.com")
    print(f"  {found}")

    # Update phone
    print("\nUpdate Bob's phone:")
    update_phone("bob@example.com", "555-9999")
    print(f"  {find_contact('bob@example.com')}")

    # Toggle favorite
    print("\nMark Alice as favorite:")
    new_val = toggle_favorite("alice@example.com")
    print(f"  favorite is now: {new_val}")
    print(f"  {find_contact('alice@example.com')}")

    # Delete
    print("\nDelete Carol:")
    delete_contact("carol@example.com")
    print("Remaining contacts:")
    for c in list_contacts():
        print(f"  {c}")

    # Expected output:
    # Adding contacts...
    #   Created: <Contact Alice Chen <alice@example.com>>, ...
    #
    # All contacts:
    #   <Contact Alice Chen <alice@example.com>>
    #   <Contact Bob Martinez <bob@example.com>>
    #   <Contact Carol Singh <carol@example.com>>
    #
    # Update Bob's phone:
    #   <Contact Bob Martinez <bob@example.com>>
    #
    # Mark Alice as favorite:
    #   favorite is now: True
    #   <Contact Alice Chen <alice@example.com> [fav]>
    #
    # Remaining contacts:
    #   <Contact Alice Chen <alice@example.com> [fav]>
    #   <Contact Bob Martinez <bob@example.com>>
