from sqlalchemy import func, desc, select, and_, distinct
from pprint import pprint

from sqlalchemy.orm import joinedload

from database.db import session
from database.models import Discipline, Grade, Group, Student, Teacher


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів"""
    result = session.query(Student.full_name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student) \
        .group_by(Student.full_name) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return result


def select_2(discipline_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = session.query(
        Discipline.discipline, Student.full_name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Discipline.discipline, Student.full_name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()

    return result


def select_3(discipline_id: int):
    """Знайти середній бал у групах з певного предмета."""
    result = session.query(
        Discipline.discipline, Group.group_name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Discipline.discipline, Group.group_name) \
        .all()

    return result


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.round(func.avg(Grade.grade)).label('avg_grade')) \
        .select_from(Grade) \
        .all()

    return f'AVG_GRADE: {result[0][0]}'


def select_5():
    """Знайти які курси читає певний викладач."""
    result = session.query(
        Discipline.id, Discipline.discipline, Teacher.full_name) \
        .select_from(Discipline) \
        .join(Teacher) \
        .all()

    return result


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    # result = session.query(
    #     Group.id, Group.group_name, Student.full_name) \
    #     .select_from(Student) \
    #     .join(Group) \
    #     .filter(Group.id == group_id) \
    #     .all()
    result = session.query(Group).options(joinedload(Group.studentinfo))

    for row in result:
        if row.id == group_id:
            return f'{row.group_name}, {[student.full_name for student in row.studentinfo]}'


def select_7(group_id, discipline_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    result = session.query(
        Group.group_name, Discipline.discipline, Student.full_name, Grade.grade) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .join(Discipline) \
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id)) \
        .all()

    return result


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = session.query(
        Teacher.full_name, Discipline.discipline, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .where(Teacher.id == teacher_id) \
        .group_by(Teacher.full_name, Discipline.discipline) \
        .all()

    return result



def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    result = session.query(
        Student.full_name, Discipline.discipline) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.id == student_id) \
        .distinct().all()

    return result


def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    result = session.query(
        Student.full_name, Teacher.full_name, Discipline.discipline) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id)) \
        .distinct().all()

    return result



def select_11(teacher_id, student_id):
    """Середній бал, який певний викладач ставить певному студентові."""
    result = session.query(
        Teacher.full_name, Student.full_name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id)) \
        .group_by(Teacher.full_name, Student.full_name) \
        .distinct().all()

    return result


def select_12(group_id, discipline_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    max_discipline_date = session.query(Grade.discipline_id, Group.id, func.max(Grade.grade_date).label('disc_max_date')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .group_by(Grade.discipline_id, Group.id) \
        .subquery()

    result = session.query(Group.group_name, Discipline.discipline, Student.full_name, Grade.grade_date, Grade.grade)\
        .select_from(Grade)\
        .join(Student) \
        .join(max_discipline_date, and_(
              Grade.discipline_id == max_discipline_date.c.discipline_id \
              ,Grade.grade_date == max_discipline_date.c.disc_max_date)) \
        .join(Discipline, Discipline.id == Grade.discipline_id) \
        .join(Group) \
        .filter(and_(Group.id == group_id, Grade.discipline_id == discipline_id)) \
        .distinct().all()

    return result


if __name__ == '__main__':
    # pprint(select_1())
    # pprint(select_2(7))
    # pprint(select_3(5))
    # pprint(select_4())
    # pprint(select_5())
    # pprint(select_6(1))
    # pprint(select_7(group_id=2, discipline_id=3))
    # pprint(select_8(3))
    # pprint(select_9(11))
    # pprint(select_10(student_id=5, teacher_id=4))
    # pprint(select_11(teacher_id=1, student_id=6))
    pprint(select_12(group_id=3, discipline_id=7))

