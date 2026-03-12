"""
Exercise: Cascade Deletes
Module 3 — Databases & SQL
Lesson 8 — Stretch Challenge
Estimated time: 20 minutes

Objective: Understand cascade delete behavior in SQLAlchemy and when to use it.

When cascade delete IS appropriate:
- Deleting a user should delete their private messages, posts, and settings
- Deleting an order should delete its line items
- Deleting a blog post should delete its comments

When cascade delete is DANGEROUS:
- Shared resources: deleting a tag used by many posts would wipe all those posts
- Audit trails: you may want to keep checkout history even after a user is deleted
- The relationship is "has-a" not "owns": a department doesn't "own" employees —
  deleting HR shouldn't delete the HR staff

ORM vs database-level cascade:
- SQLAlchemy's cascade="all, delete-orphan": handled by SQLAlchemy in Python,
  before the SQL DELETE reaches the DB
- SQL's ON DELETE CASCADE: handled by the DB engine directly, faster for large datasets
- Both achieve the same result; SQLAlchemy-level also fires model events/hooks
"""

from sqlalchemy import create_engine, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


# ============================================================
# PART 1: WITHOUT cascade — show what happens
# ============================================================

print("=" * 55)
print("PART 1: WITHOUT cascade")
print("=" * 55)

engine_no_cascade = create_engine("sqlite:///:memory:", echo=False)


class Base1(DeclarativeBase):
    pass


class AuthorNoCascade(Base1):
    __tablename__ = "authors"
    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False)
    # No cascade keyword — SQLAlchemy will raise an error if children exist
    posts: Mapped[list["PostNoCascade"]] = relationship(
        "PostNoCascade", back_populates="author"
    )


class PostNoCascade(Base1):
    __tablename__ = "posts"
    id:        Mapped[int] = mapped_column(primary_key=True)
    title:     Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author:    Mapped["AuthorNoCascade"] = relationship(
        "AuthorNoCascade", back_populates="posts"
    )


Base1.metadata.create_all(engine_no_cascade)

with Session(engine_no_cascade) as session:
    author = AuthorNoCascade(name="Emily Brontë")
    author.posts = [
        PostNoCascade(title="Wuthering Heights"),
        PostNoCascade(title="Draft Chapter 1"),
        PostNoCascade(title="Draft Chapter 2"),
    ]
    session.add(author)
    session.commit()
    author_id = author.id

    print(f"\nCreated '{author.name}' with {len(author.posts)} posts.")

    # Without cascade, SQLAlchemy raises an error when you try to delete
    # a parent that still has children loaded in the session.
    try:
        session.delete(author)
        session.commit()
        # Note: SQLAlchemy may SET author_id to NULL on children instead of raising,
        # depending on the relationship config. Let's check what actually happened.
        remaining = session.execute(
            select(PostNoCascade)
        ).scalars().all()
        orphans = [p for p in remaining if p.author_id is None]
        print(f"After delete: {len(remaining)} posts remain, {len(orphans)} are now orphans")
        print("Without cascade, children were left behind (author_id set to NULL).")
    except Exception as e:
        session.rollback()
        print(f"\nError: {type(e).__name__}: {e}")
        print("You must delete children manually first, or use cascade.")


# ============================================================
# PART 2: WITH cascade="all, delete-orphan"
# ============================================================

print("\n" + "=" * 55)
print("PART 2: WITH cascade='all, delete-orphan'")
print("=" * 55)

engine_cascade = create_engine("sqlite:///:memory:", echo=False)


class Base2(DeclarativeBase):
    pass


class Author(Base2):
    __tablename__ = "authors"
    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False)

    # cascade="all, delete-orphan" means:
    # - "all": propagate save/merge/delete/expunge operations to children
    # - "delete-orphan": also delete Posts removed from author.posts list
    #   even if the Author itself wasn't deleted (prevents dangling posts)
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Post(Base2):
    __tablename__ = "posts"
    id:        Mapped[int] = mapped_column(primary_key=True)
    title:     Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author:    Mapped["Author"] = relationship("Author", back_populates="posts")


Base2.metadata.create_all(engine_cascade)

with Session(engine_cascade) as session:
    jane = Author(name="Jane Austen")
    jane.posts = [
        Post(title="Pride and Prejudice"),
        Post(title="Sense and Sensibility"),
        Post(title="Emma"),
    ]
    session.add(jane)
    session.commit()
    author_id = jane.id

    all_posts = session.execute(select(Post)).scalars().all()
    print(f"\nBefore delete: {len(all_posts)} posts exist")
    for p in all_posts:
        print(f"  - '{p.title}'")

    print(f"\nDeleting author '{jane.name}'...")
    session.delete(jane)
    session.commit()

    remaining_posts = session.execute(select(Post)).scalars().all()
    print(f"After delete:  {len(remaining_posts)} posts remain")
    print("Cascade delete worked — all posts removed with the author. ✓")
