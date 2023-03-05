from faker import Faker

from database.db import session
from database.models import Teacher

fake_data = Faker('uk_Ua')

def create_teachers():
    for _ in range(5):
        teacher = Teacher(
            full_name=fake_data.name()
        )
        session.add(teacher)
    session.commit()


if __name__ == '__main__':
    create_teachers()