"""
Exercise: School Enrollment System
Module 3 | Lesson 8 | ~45 min

Objective:
  Model a many-to-many relationship between Students and Courses using
  SQLAlchemy. Understand how an association table links two models and
  how to traverse the relationship in both directions.
"""

from sqlalchemy import (
    create_engine, String, Integer, ForeignKey, Table, Column, select, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List, Optional

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── TODO: Uncomment and complete the association table ────────────────────────
# This table links students to courses (many-to-many).
# It has no extra columns — just two foreign keys, both part of the PK.
#
enrollments = Table(
    "enrollments",
    Base.metadata,
    Column(
        "student_id",
        Integer,
        ForeignKey("students.id"),
        primary_key=True
    ),
    Column(
        "course_id",
        Integer,
        ForeignKey("courses.id"),
        primary_key=True
    ),
)


# ── TODO: Implement the Department model ──────────────────────────────────────
# Table name: "departments"
# Columns:
#   id   — Integer, primary key
#   name — String, required, unique
# Relationship: one department -> many courses
class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    # One department can have many teachers.
    teachers: Mapped[List["Teacher"]] = relationship(
        back_populates="department"
    )

    # One department can also have many courses.
    courses: Mapped[List["Course"]] = relationship(
        back_populates="department"
    )


# ── TODO: Implement the Teacher model ─────────────────────────────────────────
# Table name: "teachers"
# Columns:
#   id            — Integer, primary key
#   name          — String, required
#   department_id — Integer, ForeignKey("departments.id")
# Relationship: many-to-one with Department; one-to-many with Course
class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    # Each teacher belongs to one department.
    department: Mapped["Department"] = relationship(
        back_populates="teachers"
    )

    # One teacher can teach multiple courses.
    courses: Mapped[List["Course"]] = relationship(
        back_populates="teacher"
    )


# ── TODO: Implement the Course model ──────────────────────────────────────────
# Table name: "courses"
# Columns:
#   id            — Integer, primary key
#   title         — String, required
#   credits       — Integer, default 3
#   department_id — Integer, ForeignKey("departments.id")
#   teacher_id    — Integer, ForeignKey("teachers.id"), nullable
# Relationships:
#   department (many-to-one)
#   teacher    (many-to-one)
#   students   (many-to-many via enrollments table)
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    teacher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teachers.id"),
        nullable=True
    )

    # Each course belongs to one department.
    department: Mapped["Department"] = relationship(
        back_populates="courses"
    )

    # A course can have one teacher.
    teacher: Mapped[Optional["Teacher"]] = relationship(
        back_populates="courses"
    )

    # A course can have many students.
    students: Mapped[List["Student"]] = relationship(
        secondary=enrollments,
        back_populates="courses"
    )

# ── TODO: Implement the Student model ─────────────────────────────────────────
# Table name: "students"
# Columns:
#   id    — Integer, primary key
#   name  — String, required
#   email — String, unique, required
#   year  — Integer (e.g. 1 = freshman, 2 = sophomore, ...)
# Relationships:
#   courses (many-to-many via enrollments, back_populates="students")
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    year: Mapped[int] = mapped_column(
        Integer
    )

    # A student can be enrolled in many courses.
    courses: Mapped[List["Course"]] = relationship(
        secondary=enrollments,
        back_populates="students"
    )


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # ── Seed ──────────────────────────────────────────────────────────────
        cs_dept  = Department(name="Computer Science")
        math_dept = Department(name="Mathematics")
        session.add_all([cs_dept, math_dept])
        session.flush()

        prof_kim   = Teacher(name="Prof. Kim",   department_id=cs_dept.id)
        prof_chen  = Teacher(name="Prof. Chen",  department_id=math_dept.id)
        session.add_all([prof_kim, prof_chen])
        session.flush()

        db101  = Course(title="Databases 101",    credits=3, department_id=cs_dept.id,   teacher_id=prof_kim.id)
        py201  = Course(title="Python Advanced",  credits=3, department_id=cs_dept.id,   teacher_id=prof_kim.id)
        calc1  = Course(title="Calculus I",       credits=4, department_id=math_dept.id, teacher_id=prof_chen.id)
        session.add_all([db101, py201, calc1])
        session.flush()

        alice = Student(name="Alice Chen",   email="alice@uni.edu", year=2)
        bob   = Student(name="Bob Martinez", email="bob@uni.edu",   year=1)
        carol = Student(name="Carol Singh",  email="carol@uni.edu", year=3)
        session.add_all([alice, bob, carol])
        session.flush()

        # Enroll students by adding courses to each student's course list.
        alice.courses.append(db101)
        alice.courses.append(py201)

        bob.courses.append(db101)
        bob.courses.append(calc1)

        # Carol is left unenrolled so we can test the final query.
        session.commit()

   # ── Demo 1: List all courses with their teacher ────────────────────────────
print("=== Courses and Teachers ===")

with Session(engine) as session:
    courses = session.scalars(select(Course)).all()

    for course in courses:
        teacher_name = course.teacher.name if course.teacher else "No teacher"
        print(f"{course.title} - {teacher_name}")

print()

   # ── Demo 2: List a student's enrolled courses ──────────────────────────────
print("=== Alice's enrolled courses ===")

with Session(engine) as session:
    alice = session.scalar(
        select(Student).where(Student.email == "alice@uni.edu")
    )

    for course in alice.courses:
        print(course.title)

print()

   # ── Demo 3: List all students in a course ─────────────────────────────────
print("=== Students in Databases 101 ===")

with Session(engine) as session:
    db101 = session.scalar(
        select(Course).where(Course.title == "Databases 101")
    )

    for student in db101.students:
        print(student.name)

print()

    # ── Demo 4: Count enrollments per course ──────────────────────────────────
print("=== Enrollment counts ===")

with Session(engine) as session:
    results = session.execute(
        select(
            Course.title,
            func.count(enrollments.c.student_id)
        )
        .outerjoin(
            enrollments,
            Course.id == enrollments.c.course_id
        )
        .group_by(Course.id)
    )

    for title, count in results:
        print(f"{title}: {count} students")

print()

   # ── Demo 5: Find students not enrolled in any course ──────────────────────
print("=== Unenrolled students ===")

with Session(engine) as session:
    students = session.scalars(
        select(Student).where(~Student.courses.any())
    ).all()

    for student in students:
        print(student.name)

print()