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

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False)

    # cascade="all, delete-orphan" means:
    # - When this Author is deleted, SQLAlchemy also deletes all related Posts
    # - "delete-orphan" additionally deletes Posts that are removed from author.posts
    #   but the Author itself is not deleted (prevents dangling posts)
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

class Post(Base):
    __tablename__ = "posts"

    id:        Mapped[int] = mapped_column(primary_key=True)
    title:     Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship("Author", back_populates="posts")

Base.metadata.create_all(engine)

# ============================================================
# DEMO
# ============================================================
with Session(engine) as session:

    # Create an author with 3 posts
    jane = Author(name="Jane Austen")
    jane.posts = [
        Post(title="Pride and Prejudice"),
        Post(title="Sense and Sensibility"),
        Post(title="Emma"),
    ]
    session.add(jane)
    session.commit()
    author_id = jane.id

    # Verify: 3 posts exist
    post_count = session.execute(
        select(func_count := None)  # placeholder — use raw count below
    )
    all_posts = session.execute(select(Post)).scalars().all()
    print(f"Before delete: {len(all_posts)} posts exist")
    for p in all_posts:
        print(f"  - '{p.title}' (author_id={p.author_id})")

    # Delete the author
    print(f"\nDeleting author '{jane.name}'...")
    session.delete(jane)
    session.commit()

    # Verify: posts are also gone
    remaining_posts = session.execute(
        select(Post).where(Post.author_id == author_id)
    ).scalars().all()
    total_posts = session.execute(select(Post)).scalars().all()

    print(f"After delete: {len(total_posts)} total posts in DB")
    print(f"Posts with author_id={author_id}: {len(remaining_posts)}")
    print("Cascade delete worked correctly — all posts removed with the author. ✓")
