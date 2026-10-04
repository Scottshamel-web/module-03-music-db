from sqlalchemy import (
    create_engine,
    String,
    Float,
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


# This creates a SQLite database file named product_catalog.db.
# echo=True is useful for this exercise because SQLAlchemy will
# print the SQL it generates in the terminal.
engine = create_engine(
    "sqlite:///product_catalog.db",
    echo=True
)


# All of our model classes will inherit from Base.
class Base(DeclarativeBase):
    pass


# This class represents the categories table.
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


# This class represents the products table.
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # For this lesson we're storing the category name as plain text.
    # We are not using a foreign key yet.
    category_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    def __repr__(self):
        return (
            f"Product(id={self.id}, "
            f"name='{self.name}', "
            f"price=${self.price:.2f}, "
            f"in_stock={self.in_stock}, "
            f"category='{self.category_name}')"
        )


# Create the tables if they are not already in the database.
Base.metadata.create_all(engine)


def add_sample_data():
    """Add categories and products to the database."""

    with Session(engine) as session:

        # Clear old sample data first so I can run the script
        # more than once without creating duplicate categories.
        session.execute(delete(Product))
        session.execute(delete(Category))
        session.commit()

        categories = [
            Category(
                name="Electronics",
                description="Computers and electronic devices"
            ),
            Category(
                name="Books",
                description="Books and learning materials"
            ),
            Category(
                name="Accessories",
                description="Computer and desk accessories"
            ),
        ]

        session.add_all(categories)

        products = [
            Product(
                name="Laptop",
                price=999.99,
                in_stock=True,
                category_name="Electronics"
            ),
            Product(
                name="Monitor",
                price=249.99,
                in_stock=True,
                category_name="Electronics"
            ),
            Product(
                name="Python Book",
                price=39.99,
                in_stock=True,
                category_name="Books"
            ),
            Product(
                name="SQL Guide",
                price=29.99,
                in_stock=False,
                category_name="Books"
            ),
            Product(
                name="Wireless Mouse",
                price=24.99,
                in_stock=True,
                category_name="Accessories"
            ),
            Product(
                name="USB-C Cable",
                price=14.99,
                in_stock=True,
                category_name="Accessories"
            ),
        ]

        session.add_all(products)

        # Nothing is permanently saved until commit() is called.
        session.commit()


def run_queries():
    """Run the three queries required by the assignment."""

    with Session(engine) as session:

        # ---------------------------------------------------------
        # Query 1: Print every category.
        # ---------------------------------------------------------
        print("\n=== All Categories ===")

        categories = session.scalars(
            select(Category)
        ).all()

        for category in categories:
            print(
                f"{category.id}: "
                f"{category.name} - "
                f"{category.description}"
            )


        # ---------------------------------------------------------
        # Query 2: Show products that are currently in stock.
        # ---------------------------------------------------------
        print("\n=== Products In Stock ===")

        in_stock_products = session.scalars(
            select(Product).where(
                Product.in_stock == True
            )
        ).all()

        for product in in_stock_products:
            print(
                f"{product.name} | "
                f"${product.price:.2f} | "
                f"{product.category_name}"
            )


        # ---------------------------------------------------------
        # Query 3: Show products that cost less than $50.
        # ---------------------------------------------------------
        print("\n=== Products Under $50 ===")

        affordable_products = session.scalars(
            select(Product)
            .where(Product.price < 50)
            .order_by(Product.price)
        ).all()

        for product in affordable_products:
            print(
                f"{product.name} | "
                f"${product.price:.2f} | "
                f"{product.category_name}"
            )


if __name__ == "__main__":
    add_sample_data()
    run_queries()