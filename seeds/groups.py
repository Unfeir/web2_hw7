from database.db import session
from database.models import Group


def create_groups():
    groups_name = ['БД-10', 'УА-15', 'Ю-7']
    for num in range(3):
        gr = Group(
            group_name=groups_name[num]
        )
        session.add(gr)
    session.commit()


if __name__ == '__main__':
    create_groups()
