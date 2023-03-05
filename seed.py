import argparse
from pprint import pprint
import psycopg2
import sqlalchemy
from sqlalchemy import update
from database.db import session
from database.models import Student, Group, Teacher, Discipline

'''
--action create -m Teacher --name 'Boris Jonson' створення вчителя
--action list -m Teacher показати всіх вчителів
--action update -m Teacher --id 3 --name 'Andry Bezos' оновити дані вчителя з id=3
--action remove -m Teacher --id 3 видалити вчителя з id=3
'''
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', required=True, help='create/list/update/remove')
parser.add_argument('-m', '--model', required=True, help ='Teacher/Student/Group/Discipline')
parser.add_argument('-v', '--value', required=False)
parser.add_argument('-n', '--name', required=False)
args = vars(parser.parse_args())
action = args.get('action').lower()
model = args.get('model').capitalize()
value = args.get('value')
name = args.get('name')

def create_(model, value, name):
    match model:
        case 'Teacher':
            data = Teacher(full_name=value)
        case 'Group':
            data = Group(group_name=value)
        case 'Student':
            data = Student(full_name=value, group_id=name)
        case 'Discipline':
            data = Discipline(discipline=value, teacher_id=name)

    try:
        session.add(data)
        session.commit()
    except Exception as err:
        return err


def list_(model, value, name):
    match model:
        case 'Teacher':
            result = session.query(Teacher.id, Teacher.full_name).select_from(Teacher).all()
            return result
        case 'Student':
            result = session.query(Student.id, Student.full_name).select_from(Student).all()
            return result
        case 'Discipline':
            result = session.query(Discipline.id, Discipline.discipline).select_from(Discipline).all()
            return result
        case 'Group':
            result = session.query(Group.id, Group.group_name).select_from(Group).all()
            return result

def update_(model, value, name):
    try:
        match model:
            case 'Teacher':
                i = session.query(Teacher.id).select_from(Teacher).filter(Teacher.full_name == value).all()
                r = session.query(Teacher).get(i[0])
                r.full_name = name
            case 'Student':
                i = session.query(Student.id).select_from(Student).filter(Student.full_name == value).all()
                r = session.query(Student).get(i[0])
                r.full_name = name
            case 'Discipline':
                i = session.query(Discipline.id).select_from(Discipline).filter(Discipline.discipline == value).all()
                r = session.query(Discipline).get(i[0])
                r.full_name = name
            case 'Group':
                i = session.query(Group.id).select_from(Group).filter(Group.group_name == value).all()
                r = session.query(Group).get(i[0])
                r.full_name = name

        session.add(r)
        session.commit()
    except Exception as err:
        return r
    finally:
        return 'Done'


def remove_(model, value, name):

    try:
        match model:
            case 'Teacher':
                i = session.query(Teacher.id).select_from(Teacher).filter(Teacher.full_name == value).all()
                r = session.query(Teacher).get(i[0])
            case 'Student':
                i = session.query(Student.id, Student.full_name).select_from(Student).filter(Student.full_name == value).all()
                r = session.query(Student).get(i[0])
            case 'Discipline':
                i = session.query(Discipline.id, Discipline.discipline).select_from(Discipline).filter(Discipline.discipline == value).all()
                r = session.query(Discipline).get(i[0])
            case 'Group':
                i = session.query(Group.id, Group.group_name).select_from(Group).filter(Group.group_name == value).all()
                r = session.query(Group).get(i[0])

        session.delete(r)
        session.commit()
        # print(vars(article))
    except Exception:
        print('no such name')
    finally:
        return 'Done'



def main():
    actions = {
        'create': create_,
        'list': list_,
        'update': update_,
        'remove': remove_
    }

    if model not in ['Teacher', 'Group', 'Student', 'Discipline']:
        return f'There is no such table: {model}'
    if action not in ['create', 'list', 'update', 'remove']:
        return f'no such command. Use --help'
    if model in ['Student', 'Discipline'] and action in ['create', 'update', 'remove'] and name is None:
        return f'You must put "n" argument with {model}'

    match model:
        case 'Teacher':
            return actions.get(action)(model, value, name)

        case 'Group':
            return actions.get(action)(model, value, name)

        case 'Student':
            return actions.get(action)(model, value, name)

        case 'Discipline':
            return actions.get(action)(model, value, name)


if __name__ == '__main__':
    pprint(main())
