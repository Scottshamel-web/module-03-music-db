from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    select,
    delete,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)


# This creates a SQLite database file in this exercise folder.
engine = create_engine(
    "sqlite:///contacts.db",
    echo=False
)


# Every model in this file will inherit from Base.
class Base(DeclarativeBase):
    pass


class Contact(Base):
    """Represents one person in the contact list."""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # Each email has to be different because we use it
    # to find, update, and delete specific contacts.
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    # Phone is optional, so it is allowed to be NULL.
    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    def __repr__(self):
        return (
            f"{self.first_name} {self.last_name} | "
            f"{self.email} | "
            f"{self.phone or 'No phone'} | "
            f"Favorite: {self.favorite}"
        )


# Create the contacts table if it does not already exist.
Base.metadata.create_all(engine)


def add_contact(first_name, last_name, email, phone=None):
    """Add a new contact."""

    with Session(engine) as session:
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )

        session.add(contact)
        session.commit()

        print(f"Added: {first_name} {last_name}")


def list_contacts():
    """Return all contacts sorted by last name."""

    with Session(engine) as session:
        contacts = session.scalars(
            select(Contact).order_by(
                Contact.last_name,
                Contact.first_name
            )
        ).all()

        return contacts


def find_contact(email):
    """Find one contact by email."""

    with Session(engine) as session:
        contact = session.scalar(
            select(Contact).where(
                Contact.email == email
            )
        )

        return contact


def update_phone(email, new_phone):
    """Change the phone number for a contact."""

    with Session(engine) as session:
        contact = session.scalar(
            select(Contact).where(
                Contact.email == email
            )
        )

        if contact is None:
            print(f"No contact found with email: {email}")
            return

        contact.phone = new_phone
        session.commit()

        print(
            f"Updated {contact.first_name}'s phone "
            f"to {new_phone}"
        )


def toggle_favorite(email):
    """Switch favorite from True to False, or False to True."""

    with Session(engine) as session:
        contact = session.scalar(
            select(Contact).where(
                Contact.email == email
            )
        )

        if contact is None:
            print(f"No contact found with email: {email}")
            return

        # "not" makes this easy:
        # False becomes True, and True becomes False.
        contact.favorite = not contact.favorite
        session.commit()

        print(
            f"{contact.first_name} favorite status: "
            f"{contact.favorite}"
        )


def delete_contact(email):
    """Remove a contact from the database."""

    with Session(engine) as session:
        contact = session.scalar(
            select(Contact).where(
                Contact.email == email
            )
        )

        if contact is None:
            print(f"No contact found with email: {email}")
            return

        name = f"{contact.first_name} {contact.last_name}"

        session.delete(contact)
        session.commit()

        print(f"Deleted: {name}")


def print_contacts(contacts):
    """Print a list of contacts in an easy-to-read format."""

    for contact in contacts:
        print(contact)


def main():

    # Clear the old sample data first so the script can be
    # run multiple times without duplicate email errors.
    with Session(engine) as session:
        session.execute(delete(Contact))
        session.commit()

    # CREATE: add at least five contacts.
    add_contact(
        "Alice",
        "Johnson",
        "alice@example.com",
        "555-111-1111"
    )

    add_contact(
        "Bob",
        "Smith",
        "bob@example.com",
        "555-222-2222"
    )

    add_contact(
        "Charlie",
        "Brown",
        "charlie@example.com"
    )

    add_contact(
        "Diana",
        "Prince",
        "diana@example.com",
        "555-444-4444"
    )

    add_contact(
        "Eve",
        "Williams",
        "eve@example.com",
        "555-555-5555"
    )


    # READ: list every contact.
    print("\n=== All Contacts ===")
    print_contacts(list_contacts())


    # READ: find one person by email.
    print("\n=== Find Contact ===")
    found = find_contact("bob@example.com")

    if found:
        print(found)


    # UPDATE: change Bob's phone number.
    print("\n=== Update Phone ===")
    update_phone(
        "bob@example.com",
        "555-999-9999"
    )


    # UPDATE: make Alice and Diana favorites.
    print("\n=== Toggle Favorites ===")
    toggle_favorite("alice@example.com")
    toggle_favorite("diana@example.com")


    # DELETE: remove Charlie.
    print("\n=== Delete Contact ===")
    delete_contact("charlie@example.com")


    # READ again to confirm all of the changes.
    print("\n=== Final Contact List ===")
    print_contacts(list_contacts())


if __name__ == "__main__":
    main()