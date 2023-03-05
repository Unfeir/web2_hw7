from random import randint
from datetime import date

from faker import Faker

from database.db import session
from database.models import Grade, Student

fake_data = Faker('uk_Ua')

def create_grades():
    students = len(session.query(Student).all())
    for student in range(1, students+1):
        for _ in range(randint(15, 20)):
            grade = Grade(
                student_id=student,
                discipline_id=randint(1, 7),
                grade_date=fake_data.date_between(date(2023,1,1), date(2023,1,31)),
                grade=randint(1, 12)
            )
            session.add(grade)
    session.commit()


if __name__ == '__main__':
    create_grades()