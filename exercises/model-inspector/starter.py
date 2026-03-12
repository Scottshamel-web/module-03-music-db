"""
Exercise: The Model Inspector
Module 3 | Lesson 6 Stretch | ~25 min

Objective:
  Use sqlalchemy.inspect() to read schema metadata at runtime —
  listing tables, columns, types, and constraints — and compare
  what the database actually has to what your models define.
"""

from sqlalchemy import create_engine, inspect, String, Float, Boolean, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import Optional, List

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── Fully defined models (provided — these are your setup, not your solution) ──

class Category(Base):
    __tablename__ = "categories"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name!r}>"


class Product(Base):
    __tablename__ = "products"

    id:          Mapped[int]           = mapped_column(Integer, primary_key=True)
    name:        Mapped[str]           = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price:       Mapped[float]         = mapped_column(Float, nullable=False)
    in_stock:    Mapped[bool]          = mapped_column(Boolean, default=True)
    category_id: Mapped[int]           = mapped_column(Integer, ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product id={self.id} name={self.name!r} price={self.price}>"


# ── Create tables and seed a little data ─────────────────────────────────────
Base.metadata.create_all(engine)

with Session(engine) as session:
    cat = Category(name="Electronics")
    session.add(cat)
    session.flush()
    session.add(Product(name="Wireless Headphones", price=79.99, category_id=cat.id))
    session.add(Product(name="USB-C Hub",           price=39.99, category_id=cat.id, in_stock=False))
    session.commit()


# ── Your tasks ────────────────────────────────────────────────────────────────

# Task 1: Use inspect() to list all table names in the database
print("=== Tables in the database ===")
# TODO: create an Inspector with inspect(engine)
# TODO: call .get_table_names() and print each table name
# inspector = inspect(engine)
# for table_name in ...:
#     print(f"  {table_name}")
print()

# Task 2: For each table, print column details
print("=== Column details ===")
# TODO: loop through each table
# TODO: for each table, call inspector.get_columns(table_name)
# Each column dict has keys: 'name', 'type', 'nullable', 'default', 'primary_key'
# for table_name in ...:
#     print(f"\nTable: {table_name}")
#     for col in inspector.get_columns(table_name):
#         print(f"  {col['name']:<20} type={col['type']}  nullable={col['nullable']}")
print()

# Task 3: Print foreign key information for each table
print("=== Foreign keys ===")
# TODO: call inspector.get_foreign_keys(table_name) for each table
# Each FK dict has: 'constrained_columns', 'referred_table', 'referred_columns'
# for table_name in ...:
#     fks = inspector.get_foreign_keys(table_name)
#     if fks:
#         print(f"\nTable: {table_name}")
#         for fk in fks:
#             print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
print()

# Task 4: Verify your findings match the model definitions above.
# Write a few print() statements that compare the inspected schema
# to the Mapped[] annotations in the model classes.
# Example: confirm 'products' has columns 'price' and 'in_stock'.
print("=== Verification ===")
# TODO: your comparison here
pass

# Expected output (partial):
# === Tables in the database ===
#   categories
#   products
#
# === Column details ===
#
# Table: categories
#   id                   type=INTEGER  nullable=False
#   name                 type=VARCHAR  nullable=False
#
# Table: products
#   id                   type=INTEGER  nullable=False
#   name                 type=VARCHAR  nullable=False
#   description          type=VARCHAR  nullable=True
#   price                type=FLOAT    nullable=False
#   in_stock             type=BOOLEAN  nullable=True
#   category_id          type=INTEGER  nullable=True
#
# === Foreign keys ===
#
# Table: products
#   ['category_id'] -> categories.['id']
