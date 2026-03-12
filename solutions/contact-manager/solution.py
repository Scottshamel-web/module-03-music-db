"""
Exercise: Contact Manager
Module 3 — Databases & SQL
Lesson 7 — Practice Exercise
Estimated time: 35 minutes

Objective: Build a full CRUD contact manager using SQLAlchemy 2.0 sessions.
Understand when to call commit() vs flush(), and how sessions manage state.
"""

from sqlalchemy import create_engine, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

    id:         Mapped[int]        = mapped_column(primary_key=True)
    first_name: Mapped[str]        = mapped_column(String(100), nullable=False)
    last_name:  Mapped[str]        = mapped_column(String(100), nullable=False)
    email:      Mapped[str]        = mapped_column(String(200), unique=True, nullable=False)
    phone:      Mapped[str | None] = mapped_column(String(20))      # optional
    favorite:   Mapped[bool]       = mapped_column(Boolean, default=False)

    def __repr__(self):
        fav = "★" if self.favorite else " "
        return f"[{fav}] {self.first_name} {self.last_name} <{self.email}>"

Base.metadata.create_all(engine)

# ============================================================
# CRUD FUNCTIONS
# Each function opens its own Session context manager.
# Session tracks all objects loaded or added within it.
# ============================================================

def add_contact(first_name, last_name, email, phone=None):
    """Add a new contact. Returns the created Contact."""
    with Session(engine) as session:
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        session.add(contact)
        # session.commit() flushes pending changes AND ends the transaction.
        # After commit, the data is durably saved to the database.
        session.commit()
        session.refresh(contact)  # reload to get the auto-generated id
        return contact

def list_contacts():
    """Return all contacts sorted by last name, then first name."""
    with Session(engine) as session:
        return session.execute(
            select(Contact).order_by(Contact.last_name, Contact.first_name)
        ).scalars().all()

def find_contact(email):
    """Find a single contact by email. Returns Contact or None."""
    with Session(engine) as session:
        return session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()

def update_phone(email, new_phone):
    """Update the phone number for a contact. Returns True if found, False if not."""
    with Session(engine) as session:
        contact = session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact:
            return False
        contact.phone = new_phone
        # session.flush() writes the change to the DB within the current transaction
        # but doesn't commit — useful if you need the updated value for another operation
        # in the same transaction. Here we just commit directly.
        session.commit()
        return True

def toggle_favorite(email):
    """Flip a contact's favorite status. Returns the new status or None if not found."""
    with Session(engine) as session:
        contact = session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact:
            return None
        contact.favorite = not contact.favorite
        session.commit()
        return contact.favorite

def delete_contact(email):
    """Delete a contact by email. Returns True if deleted, False if not found."""
    with Session(engine) as session:
        contact = session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact:
            return False
        session.delete(contact)
        session.commit()
        return True

# ============================================================
# HELPER
# ============================================================

def print_contacts():
    contacts = list_contacts()
    if not contacts:
        print("  (no contacts)")
        return
    for c in contacts:
        fav = "★ " if c.favorite else "  "
        phone = c.phone or "—"
        print(f"  {fav}{c.first_name} {c.last_name:<15} {c.email:<30} {phone}")

# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Add 5 contacts
    print("Adding contacts...")
    add_contact("Alice", "Chen",    "alice@example.com",   "555-0101")
    add_contact("Bob",   "Martinez","bob@example.com",     "555-0102")
    add_contact("Carol", "Davis",   "carol@example.com")   # no phone
    add_contact("Dan",   "Wilson",  "dan@example.com",     "555-0104")
    add_contact("Eva",   "Brown",   "eva@example.com",     "555-0105")

    print("\nAll contacts:")
    print_contacts()

    # Update a phone
    print("\nUpdating Carol's phone to 555-0103...")
    update_phone("carol@example.com", "555-0103")

    # Toggle favorites
    print("Marking Alice and Eva as favorites...")
    toggle_favorite("alice@example.com")
    toggle_favorite("eva@example.com")

    # Delete one
    print("Deleting Dan Wilson...")
    delete_contact("dan@example.com")

    print("\nFinal contacts:")
    print_contacts()

    # Look up a specific contact
    print("\nLooking up alice@example.com:")
    c = find_contact("alice@example.com")
    print(f"  Found: {c.first_name} {c.last_name}, favorite={c.favorite}, phone={c.phone}")
