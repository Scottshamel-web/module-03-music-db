"""
Module 3 Project: Library Management System
library_system.py — Complete solution

Uses an in-memory SQLite database so it runs cleanly without leaving a .db file.
Implements all models, CRUD operations, and query functions using SQLAlchemy 2.0 patterns.
"""

from sqlalchemy import (
    create_engine, String, Integer, Boolean, ForeignKey,
    Table, Column, Date, select, func, and_
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import date, timedelta
from typing import Optional, List

# Use in-memory SQLite for a clean, file-free demo.
# Switch to "sqlite:///library.db" if you want persistence.
engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# Association table for the Book <-> Genre many-to-many relationship.
# We use a plain Table (not a model class) because it has no extra columns.
book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id",  Integer, ForeignKey("books.id"),  primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"

    id:   Mapped[int]           = mapped_column(Integer, primary_key=True)
    name: Mapped[str]           = mapped_column(String, nullable=False)
    bio:  Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # One author -> many books
    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

    def __repr__(self) -> str:
        return f"<Author id={self.id} name={self.name!r}>"


class Genre(Base):
    __tablename__ = "genres"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Many genres <-> many books (via association table)
    books: Mapped[List["Book"]] = relationship("Book", secondary=book_genres, back_populates="genres")

    def __repr__(self) -> str:
        return f"<Genre id={self.id} name={self.name!r}>"


class Book(Base):
    __tablename__ = "books"

    id:             Mapped[int]           = mapped_column(Integer, primary_key=True)
    title:          Mapped[str]           = mapped_column(String, nullable=False)
    isbn:           Mapped[str]           = mapped_column(String, unique=True, nullable=False)
    published_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    author_id:      Mapped[int]           = mapped_column(Integer, ForeignKey("authors.id"), nullable=False)
    available:      Mapped[bool]          = mapped_column(Boolean, default=True, nullable=False)

    # Many-to-one: each book has one author
    author: Mapped["Author"] = relationship("Author", back_populates="books")

    # Many-to-many: a book can belong to multiple genres
    genres: Mapped[List["Genre"]] = relationship("Genre", secondary=book_genres, back_populates="books")

    # One book -> many checkout records
    checkouts: Mapped[List["Checkout"]] = relationship("Checkout", back_populates="book")

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r} available={self.available}>"


class Borrower(Base):
    __tablename__ = "borrowers"

    id:    Mapped[int]           = mapped_column(Integer, primary_key=True)
    name:  Mapped[str]           = mapped_column(String, nullable=False)
    email: Mapped[str]           = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # One borrower -> many checkouts
    checkouts: Mapped[List["Checkout"]] = relationship("Checkout", back_populates="borrower")

    def __repr__(self) -> str:
        return f"<Borrower id={self.id} name={self.name!r} email={self.email!r}>"


class Checkout(Base):
    __tablename__ = "checkouts"

    id:            Mapped[int]           = mapped_column(Integer, primary_key=True)
    book_id:       Mapped[int]           = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id:   Mapped[int]           = mapped_column(Integer, ForeignKey("borrowers.id"), nullable=False)
    checkout_date: Mapped[date]          = mapped_column(Date, nullable=False)
    due_date:      Mapped[date]          = mapped_column(Date, nullable=False)
    return_date:   Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # NULL = not yet returned

    # Relationships back to book and borrower
    book:     Mapped["Book"]     = relationship("Book",     back_populates="checkouts")
    borrower: Mapped["Borrower"] = relationship("Borrower", back_populates="checkouts")

    def __repr__(self) -> str:
        returned = self.return_date or "not returned"
        return f"<Checkout id={self.id} book_id={self.book_id} due={self.due_date} returned={returned}>"


def init_db():
    """Create all database tables. Call this before using any other functions."""
    Base.metadata.create_all(engine)


# ============================================================
# CRUD FUNCTIONS
# ============================================================

def add_author(name: str, bio: str = None) -> Author:
    """Add a new author. Returns the created Author object."""
    with Session(engine) as session:
        author = Author(name=name, bio=bio)
        session.add(author)
        session.commit()
        session.refresh(author)
        return author


def add_book(title: str, isbn: str, author_id: int,
             published_year: int = None, genre_names: list = None) -> Book:
    """
    Add a new book. Assigns genres by name (creates the genre if it doesn't exist yet).
    Returns the created Book object.
    """
    with Session(engine) as session:
        book = Book(
            title=title,
            isbn=isbn,
            author_id=author_id,
            published_year=published_year,
            available=True,
        )

        # Resolve genre names -> Genre objects, creating new ones as needed
        if genre_names:
            for genre_name in genre_names:
                genre = session.execute(
                    select(Genre).where(Genre.name == genre_name)
                ).scalar_one_or_none()
                if genre is None:
                    genre = Genre(name=genre_name)
                    session.add(genre)
                book.genres.append(genre)

        session.add(book)
        session.commit()
        session.refresh(book)
        return book


def add_borrower(name: str, email: str, phone: str = None) -> Borrower:
    """Register a new borrower. Returns the created Borrower object."""
    with Session(engine) as session:
        borrower = Borrower(name=name, email=email, phone=phone)
        session.add(borrower)
        session.commit()
        session.refresh(borrower)
        return borrower


def checkout_book(book_id: int, borrower_id: int, days: int = 14) -> Checkout:
    """
    Check out a book. Sets book.available = False. due_date = today + days.
    Raises ValueError if the book is not available.
    Returns the created Checkout object.
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            raise ValueError(f"Book with id={book_id} does not exist.")
        if not book.available:
            raise ValueError(f"Book '{book.title}' is not currently available.")

        today = date.today()
        checkout = Checkout(
            book_id=book_id,
            borrower_id=borrower_id,
            checkout_date=today,
            due_date=today + timedelta(days=days),
        )
        book.available = False
        session.add(checkout)
        session.commit()
        session.refresh(checkout)
        return checkout


def return_book(checkout_id: int) -> Checkout:
    """
    Return a book. Sets book.available = True, sets return_date = today.
    Returns the updated Checkout object.
    """
    with Session(engine) as session:
        checkout = session.get(Checkout, checkout_id)
        if checkout is None:
            raise ValueError(f"Checkout with id={checkout_id} does not exist.")

        checkout.return_date = date.today()
        checkout.book.available = True
        session.commit()
        session.refresh(checkout)
        return checkout


# ============================================================
# QUERY FUNCTIONS
# ============================================================

def find_books_by_author(author_name: str) -> list:
    """Return all books whose author name contains author_name (case-insensitive)."""
    with Session(engine) as session:
        stmt = (
            select(Book)
            .join(Book.author)
            .where(Author.name.ilike(f"%{author_name}%"))
        )
        return session.execute(stmt).scalars().all()


def get_overdue_books() -> list:
    """Return all Checkout objects where due_date < today and return_date is None."""
    with Session(engine) as session:
        today = date.today()
        stmt = select(Checkout).where(
            and_(
                Checkout.due_date < today,
                Checkout.return_date.is_(None),
            )
        )
        return session.execute(stmt).scalars().all()


def get_popular_genres(limit: int = 3) -> list:
    """
    Return the top `limit` genres by checkout count.
    Returns a list of (Genre.name, checkout_count) tuples.
    """
    with Session(engine) as session:
        stmt = (
            select(Genre.name, func.count(Checkout.id).label("checkout_count"))
            .join(book_genres, Genre.id == book_genres.c.genre_id)
            .join(Book, Book.id == book_genres.c.book_id)
            .join(Checkout, Checkout.book_id == Book.id)
            .group_by(Genre.id)
            .order_by(func.count(Checkout.id).desc())
            .limit(limit)
        )
        return session.execute(stmt).all()


def get_available_books() -> list:
    """Return all Book objects where available == True."""
    with Session(engine) as session:
        stmt = select(Book).where(Book.available == True)
        return session.execute(stmt).scalars().all()
