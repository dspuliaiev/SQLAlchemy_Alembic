from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from conf.models import Student, Group, Teacher, Subject, Grade
import random
from conf.db import URI


# Підключення до бази даних
engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)
Session = sessionmaker(bind=engine)
session = Session()

# Створення екземпляру Faker
fake = Faker()

# Створення студентів
def create_students(num_students, group_id=None):
    students = []
    for _ in range(num_students):
        student = Student(
            fullname=fake.name(),
            group=group_id
        )
        students.append(student)
    return students

# Створення груп
def create_groups(num_groups):
    groups = []
    for i in range(1, num_groups + 1):
        group = Group(name=f'Group {i}')
        groups.append(group)
    return groups

# Створення викладачів
def create_teachers(num_teachers):
    teachers = []
    for _ in range(num_teachers):
        teacher = Teacher(fullname=fake.name())
        teachers.append(teacher)
    return teachers

# Створення дисциплін
def create_subjects(num_subjects, teachers):
    subjects = []
    for _ in range(num_subjects):
        teacher = random.choice(teachers)
        subject = Subject(
            name=fake.word(),
            teacher=teacher
        )
        subjects.append(subject)
    return subjects

# Створення оцінок
def create_grades(students, subjects):
    grades = []
    for student in students:
        for subject in subjects:
            grade_date = fake.date_time_between(start_date='-30d', end_date='now')
            grade = Grade(
                grade=fake.random_int(min=1, max=100),
                grade_date=fake.date_between(start_date='-1y', end_date='today'),
                student=student,
                discipline=subject
            )
            grades.append(grade)
    return grades

# Створення студентів, груп, вчителів, предметів та оцінок
def seed_database():
    num_students = 30
    num_groups = 3
    num_teachers = 5
    num_subjects = 8

    students = create_students(num_students)
    groups = create_groups(num_groups)
    teachers = create_teachers(num_teachers)
    subjects = create_subjects(num_subjects, teachers)

    # Додавання об'єктів до сесії
    session.add_all(students)
    session.add_all(groups)
    session.add_all(teachers)
    session.add_all(subjects)

    # Застосування змін у базі даних
    session.commit()

    # Створення оцінок
    grades = create_grades(students, subjects)
    session.add_all(grades)
    session.commit()

if __name__ == "__main__":
    seed_database()