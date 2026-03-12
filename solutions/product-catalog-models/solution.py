"""
Exercise: Product Catalog Models
Module 3 — Databases & SQL
Lesson 6 — Practice Exercise
Estimated time: 35 minutes

Objective: Define SQLAlchemy models using the ORM (Object-Relational Mapper),
create tables from them, and query data using Python instead of raw SQL strings.

ORM vs raw SQL:
- Raw SQL: you write "SELECT * FROM products WHERE in_stock = 1" as a string
- ORM: you write session.execute(select(Product).where(Product.in_stock == True))
- ORM benefits: Python objects instead of tuples, IDE autocomplete, easier to refactor
- ORM trade-off: adds complexity, can hide what SQL is actually running
"""

from sqlalchemy import create_engine, String, Float, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# In-memory SQLite — clean slate on every run, nothing persists to disk
engine = create_engine("sqlite:///:memory:", echo=False)
# Set echo=True to see the SQL SQLAlchemy generates — great for learning!
# echo=True would print: CREATE TABLE, INSERT, SELECT as SQLAlchemy runs them

# ============================================================
# DEFINE MODELS
# SQLAlchemy 2.0 pattern: inherit from DeclarativeBase
# Each class = one table; each Mapped[type] = one column
# ============================================================

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"

    id:          Mapped[int]   = mapped_column(primary_key=True)
    name:        Mapped[str]   = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(500))  # optional (nullable)

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name!r})"

class Product(Base):
    __tablename__ = "products"

    id:            Mapped[int]   = mapped_column(primary_key=True)
    name:          Mapped[str]   = mapped_column(String(200), nullable=False)
    price:         Mapped[float] = mapped_column(Float, nullable=False)
    in_stock:      Mapped[bool]  = mapped_column(Boolean, default=True)
    # Storing category as a plain text field here — no FK yet (that comes in Lesson 8)
    category_name: Mapped[str | None] = mapped_column(String(100))

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name!r}, price={self.price})"

# ============================================================
# CREATE TABLES
# Base.metadata knows about all models defined above.
# create_all() issues the CREATE TABLE statements.
# ============================================================
Base.metadata.create_all(engine)

# ============================================================
# INSERT DATA
# Session manages a unit of work — changes aren't written to the DB
# until you call session.commit(). session.add() stages an object.
# ============================================================
with Session(engine) as session:
    categories = [
        Category(name="Electronics",     description="Devices and gadgets"),
        Category(name="Books",           description="Fiction and non-fiction"),
        Category(name="Home & Garden",   description="Home improvement and decor"),
    ]
    session.add_all(categories)

    products = [
        Product(name="Laptop Pro",        price=1299.00, category_name="Electronics"),
        Product(name="Wireless Mouse",    price=39.99,   category_name="Electronics"),
        Product(name="Python Crash Course", price=29.99, category_name="Books"),
        Product(name="Clean Code",        price=34.99,   category_name="Books"),
        Product(name="AI Engineering",    price=49.99,   category_name="Books"),
        Product(name="Desk Lamp",         price=29.99,   category_name="Home & Garden"),
        Product(name="Webcam HD",         price=79.99,   category_name="Electronics",
                in_stock=False),
        Product(name="Succulent Plant",   price=12.99,   category_name="Home & Garden"),
    ]
    session.add_all(products)
    session.commit()

# ============================================================
# QUERIES
# select(Model) is SQLAlchemy 2.0's way of building SELECT statements.
# .scalars().all() returns a list of model objects (not raw tuples).
# ============================================================
with Session(engine) as session:

    # All categories
    print("All categories:")
    cats = session.execute(select(Category).order_by(Category.name)).scalars().all()
    for c in cats:
        print(f"  {c.id}: {c.name} — {c.description}")

    # In-stock products only
    print("\nIn-stock products:")
    in_stock = session.execute(
        select(Product).where(Product.in_stock == True).order_by(Product.name)
    ).scalars().all()
    for p in in_stock:
        print(f"  {p.name:<30} ${p.price:.2f}  ({p.category_name})")

    # Products under $50
    print("\nProducts under $50:")
    cheap = session.execute(
        select(Product).where(Product.price < 50).order_by(Product.price)
    ).scalars().all()
    for p in cheap:
        stock = "✓" if p.in_stock else "✗"
        print(f"  [{stock}] {p.name:<30} ${p.price:.2f}")
