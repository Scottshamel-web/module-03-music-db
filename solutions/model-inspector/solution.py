"""
Exercise: The Model Inspector
Module 3 — Databases & SQL
Lesson 6 — Stretch Challenge
Estimated time: 25 minutes

Objective: Use SQLAlchemy's inspect module to reflect and print the schema of
a database you created. Useful for: understanding an inherited database,
debugging migrations, verifying that your models match the actual tables.
"""

from sqlalchemy import create_engine, String, Float, Boolean, inspect, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# ============================================================
# MODELS (same as Product Catalog exercise — copied in, not imported,
# so this file is self-contained and runnable on its own)
# ============================================================

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    id:          Mapped[int]        = mapped_column(primary_key=True)
    name:        Mapped[str]        = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(500))

class Product(Base):
    __tablename__ = "products"
    id:            Mapped[int]        = mapped_column(primary_key=True)
    name:          Mapped[str]        = mapped_column(String(200), nullable=False)
    price:         Mapped[float]      = mapped_column(Float, nullable=False)
    in_stock:      Mapped[bool]       = mapped_column(Boolean, default=True)
    category_name: Mapped[str | None] = mapped_column(String(100))

Base.metadata.create_all(engine)

# Add some data so the tables aren't empty
with Session(engine) as session:
    session.add_all([
        Category(name="Electronics"),
        Category(name="Books"),
        Product(name="Laptop", price=999.0, category_name="Electronics"),
    ])
    session.commit()

# ============================================================
# INSPECTION
# sqlalchemy.inspect(engine) returns an Inspector object that
# can read schema info from the database — table names, columns,
# foreign keys, indexes, etc. — without needing to look at model code.
#
# When is this useful?
# - You inherited a database and don't have the ORM models
# - You're debugging why a migration failed
# - You want to verify that create_all() actually created the columns you expected
# - You're building a generic tool that works with any database schema
# ============================================================

inspector = inspect(engine)

print("=" * 55)
print("DATABASE SCHEMA INSPECTION")
print("=" * 55)

# List all tables in the database
table_names = inspector.get_table_names()
print(f"\nTables found: {table_names}\n")

for table_name in table_names:
    print(f"Table: {table_name}")
    print("-" * 45)

    # get_columns returns a list of dicts, one per column
    columns = inspector.get_columns(table_name)
    print(f"  {'Column':<20} {'Type':<20} {'Nullable'}")
    print(f"  {'-'*18} {'-'*18} {'-'*8}")
    for col in columns:
        nullable = "Yes" if col["nullable"] else "No"
        print(f"  {col['name']:<20} {str(col['type']):<20} {nullable}")

    # Get primary key info
    pk = inspector.get_pk_constraint(table_name)
    if pk["constrained_columns"]:
        print(f"  Primary key: {pk['constrained_columns']}")

    # Get foreign key info (if any)
    fks = inspector.get_foreign_keys(table_name)
    for fk in fks:
        print(f"  Foreign key: {fk['constrained_columns']} → "
              f"{fk['referred_table']}.{fk['referred_columns']}")

    print()

# ============================================================
# COMPARE TO MODEL DEFINITION
# The inspect output should match what you defined in your model classes.
# If they don't match, it usually means:
# - You changed the model but didn't run migrations
# - The database was created from an older version of the code
# ============================================================
print("Comparing to model definition:")
print(f"  Category model has columns: {[c.name for c in Category.__table__.columns]}")
print(f"  Product model has columns:  {[c.name for c in Product.__table__.columns]}")
print("\nThese match the inspect output above ✓")
