"""
Exercise: Cascade Deletes
Module 3 | Lesson 8 Stretch | ~20 min

Objective:
  Understand and implement cascade delete behavior in SQLAlchemy.
  When a parent object is deleted, cascade="all, delete-orphan" ensures
  that related child objects are automatically deleted rather than left
  as orphaned rows with broken foreign keys.
"""

from sqlalchemy import create_engine, String, Integer, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── TODO: Implement the Author model ─────────────────────────────────────────
# Table name: "authors"
# Columns: id (PK), name (String, required)
# Relationship: one author -> many posts
# The cascade should be set on THIS side of the relationship so that
# deleting an author automatically deletes all their posts.
class Author(Base):
    __tablename__ = "authors"
    # TODO: define id and name columns
    # TODO: add relationship to Post
    # TODO: add cascade="all, delete-orphan" to the relationship
    # Example:
    #   posts: Mapped[List["Post"]] = relationship(
    #       "Post", back_populates="author", cascade="all, delete-orphan"
    #   )
    pass


# ── TODO: Implement the Post model ────────────────────────────────────────────
# Table name: "posts"
# Columns:
#   id        — Integer, primary key
#   title     — String, required
#   author_id — Integer, ForeignKey("authors.id")
# Relationship: many-to-one back to Author
class Post(Base):
    __tablename__ = "posts"
    # TODO: define columns
    # TODO: add relationship back to Author
    pass


# ── Demo block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # ── Create an author with posts ───────────────────────────────────────────
    with Session(engine) as session:
        # TODO: create an Author named "Alice"
        # TODO: create 3 Post objects linked to Alice
        # TODO: add and commit
        pass

    # ── Verify posts exist before deletion ────────────────────────────────────
    with Session(engine) as session:
        post_count = session.execute(select(Post)).scalars().all()
        print(f"Posts before deletion: {len(post_count)}")
        # Expected: Posts before deletion: 3

    # ── Delete the author ─────────────────────────────────────────────────────
    with Session(engine) as session:
        # TODO: load Alice by name and delete her
        # TODO: commit
        pass

    # ── Verify posts were also deleted (cascade worked) ───────────────────────
    with Session(engine) as session:
        post_count = session.execute(select(Post)).scalars().all()
        print(f"Posts after deletion: {len(post_count)}")
        # Expected: Posts after deletion: 0

        author_count = session.execute(select(Author)).scalars().all()
        print(f"Authors after deletion: {len(author_count)}")
        # Expected: Authors after deletion: 0

    print("\nCascade delete verified successfully!")

    # ── What happens WITHOUT cascade? ─────────────────────────────────────────
    # If you remove cascade="all, delete-orphan" from the relationship,
    # SQLAlchemy will raise an error (or leave orphaned rows if you bypass it).
    # Try it: comment out the cascade parameter and observe the difference.
