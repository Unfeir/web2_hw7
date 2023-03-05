from faker import Faker
from random import randint

from database.db import session
from database.models import Discipline

fake_data = Faker('uk_Ua')

def create_disciplines():
    for _ in range(7):
        discipline = Discipline(
            discipline=f'факультет - {fake_data.country()} знавства',
            teacher_id=randint(1, 5)
        )
        session.add(discipline)
    session.commit()


if __name__ == '__main__':
    create_disciplines()