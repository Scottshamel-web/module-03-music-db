"""
Exercise: School Enrollment System
Module 3 — Databases & SQL
Lesson 8 — Practice Exercise
Estimated time: 45 minutes

Objective: Model a many-to-many relationship (students ↔ courses) using
SQLAlchemy's relationship() and an association table. Understand back_populates.
"""

from sqlalchemy import create_engine, String, ForeignKey, Table, Column, Integer, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

# ============================================================
# ASSOCIATION TABLE for Many-to-Many: Student ↔ Course
# A student can be enrolled in many courses.
# A course can have many enrolled students.
# The association table holds (student_id, course_id) pairs.
# This is NOT a model class — it's a plain Table object because
# it has no extra columns beyond the two foreign keys.
# ============================================================
student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id",  Integer, ForeignKey("courses.id"),  primary_key=True),
)

class Department(Base):
    __tablename__ = "departments"

    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # One department has many teachers
    # back_populates="department" means Teacher has a `.department` attribute
    # that points back to this Department
    teachers: Mapped[list["Teacher"]] = relationship("Teacher", back_populates="department")

class Teacher(Base):
    __tablename__ = "teachers"

    id:            Mapped[int]      = mapped_column(primary_key=True)
    name:          Mapped[str]      = mapped_column(String(100), nullable=False)
    department_id: Mapped[int]      = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship("Department", back_populates="teachers")
    courses:    Mapped[list["Course"]] = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = "courses"

    id:         Mapped[int] = mapped_column(primary_key=True)
    title:      Mapped[str] = mapped_column(String(200), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    teacher:  Mapped["Teacher"]         = relationship("Teacher", back_populates="courses")
    # secondary= points to the association table for the M2M join
    students: Mapped[list["Student"]]   = relationship(
        "Student", secondary=student_courses, back_populates="courses"
    )

class Student(Base):
    __tablename__ = "students"

    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        "Course", secondary=student_courses, back_populates="students"
    )

Base.metadata.create_all(engine)

# ============================================================
# POPULATE
# ============================================================
with Session(engine) as session:
    # Departments
    cs   = Department(name="Computer Science")
    math = Department(name="Mathematics")
    session.add_all([cs, math])
    session.flush()  # flush to get IDs before creating teachers

    # Teachers
    t1 = Teacher(name="Dr. Alice Park",    department=cs)
    t2 = Teacher(name="Prof. Bob Chen",    department=cs)
    t3 = Teacher(name="Dr. Carol White",   department=math)
    t4 = Teacher(name="Prof. Dan Rivera",  department=math)
    session.add_all([t1, t2, t3, t4])
    session.flush()

    # Courses
    c1 = Course(title="Intro to Python",        teacher=t1)
    c2 = Course(title="Data Structures",         teacher=t1)
    c3 = Course(title="Web Development",         teacher=t2)
    c4 = Course(title="Calculus I",              teacher=t3)
    c5 = Course(title="Linear Algebra",          teacher=t4)
    session.add_all([c1, c2, c3, c4, c5])
    session.flush()

    # Students with varied enrollments
    s1 = Student(name="Zoe Adams",   email="zoe@school.edu",   courses=[c1, c2, c3])
    s2 = Student(name="Raj Patel",   email="raj@school.edu",   courses=[c1, c4])
    s3 = Student(name="Nina Brown",  email="nina@school.edu",  courses=[c2, c3, c5])
    s4 = Student(name="Marco Diaz",  email="marco@school.edu", courses=[c1])
    s5 = Student(name="Yuki Tanaka", email="yuki@school.edu",  courses=[c4, c5])
    s6 = Student(name="Olu Okafor",  email="olu@school.edu",   courses=[c1, c2, c4])
    session.add_all([s1, s2, s3, s4, s5, s6])
    session.commit()

# ============================================================
# DEMONSTRATIONS
# ============================================================
with Session(engine) as session:

    # 1. Each department and its teachers
    print("1. Departments and their teachers:")
    depts = session.execute(select(Department).order_by(Department.name)).scalars().all()
    for dept in depts:
        print(f"   {dept.name}:")
        for teacher in dept.teachers:
            print(f"     - {teacher.name}")

    # 2. Each teacher and their courses
    print("\n2. Teachers and their courses:")
    teachers = session.execute(select(Teacher).order_by(Teacher.name)).scalars().all()
    for t in teachers:
        courses = ", ".join(c.title for c in t.courses) or "(no courses)"
        print(f"   {t.name}: {courses}")

    # 3. Each course with enrolled students
    print("\n3. Courses with enrolled students:")
    courses = session.execute(select(Course).order_by(Course.title)).scalars().all()
    for c in courses:
        students = ", ".join(s.name for s in c.students) or "(no students)"
        print(f"   {c.title} ({len(c.students)} students): {students}")

    # 4. Each student and their courses
    print("\n4. Students and their enrolled courses:")
    students = session.execute(select(Student).order_by(Student.name)).scalars().all()
    for s in students:
        courses = ", ".join(c.title for c in s.courses)
        print(f"   {s.name}: {courses}")

    # 5. Courses with more than 2 students enrolled
    print("\n5. Courses with more than 2 enrolled students:")
    results = session.execute(
        select(Course.title, func.count(Student.id).label("student_count"))
        .join(student_courses, Course.id == student_courses.c.course_id)
        .join(Student, Student.id == student_courses.c.student_id)
        .group_by(Course.id)
        .having(func.count(Student.id) > 2)
        .order_by(func.count(Student.id).desc())
    ).all()
    for title, count in results:
        print(f"   {title}: {count} students")
