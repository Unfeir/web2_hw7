from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Date

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50))

    studentinfo = relationship('Student', back_populates='groupinfo')


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))

    groupinfo = relationship('Group', back_populates='studentinfo')
    gradeinfo = relationship('Grade', back_populates='studentinfo')


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)

    disciplineinfo = relationship('Discipline', back_populates='teacherinfo')


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    discipline = Column(String(150), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)

    teacherinfo = relationship('Teacher', back_populates='disciplineinfo')
    gradeinfo = relationship('Grade', back_populates='disciplineinfo')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    discipline_id = Column(Integer, ForeignKey('disciplines.id', ondelete='CASCADE'), nullable=False)
    grade_date = Column(Date)
    grade = Column(Integer)

    studentinfo = relationship('Student', back_populates='gradeinfo')
    disciplineinfo = relationship('Discipline', back_populates='gradeinfo')
