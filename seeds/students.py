from faker import Faker
from random import randint

from database.db import session
from database.models import Student

fake_data = Faker('uk_UA')


def create_students():
    for _ in range(50):
        student = Student(
            full_name=fake_data.name(),
            group_id=randint(1, 3)
        )
        session.add(student)
    session.commit()


if __name__ == '__main__':
    create_students()
