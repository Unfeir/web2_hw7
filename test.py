# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.orm import joinedload
#
# from database.db import session, engine
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(20))
#     articles = relationship('Article', back_populates='author')
#
#
# class Article(Base):
#     __tablename__ = 'articles'
#     id = Column(Integer(), primary_key=True)
#     title = Column(String(255))
#     content = Column(Text())
#     user_id = Column(Integer(), ForeignKey('users.id'))
#     author = relationship('User', back_populates='articles')
# #
# # Base.metadata.create_all(engine)
# # Base.metadata.bind = engine
# #
# # new_person = User(name="Bill")
# # session.add(new_person)
# #
# # session.commit()
# #
# # new_address = Article(title='some_title', content='CONTEXTY', user_id=2)
# # session.add(new_address)
# # session.commit()
#
# users= session.query(User).all()
#
# # for user in users:
# #     for article in user.articles:
# #         print(article.title, user.name)
#
#
# users = session.query(User).options(joinedload(User.articles)).all()
# for i in users:
#     print(vars(i))
#
#


from database.db import session
from database.models import Group, Student
from sqlalchemy.orm import joinedload

# groups = session.query(Group).all()
# for gr in groups:
#     for student in gr.studentinfo:
#         print(gr.group_name, student.full_name)


groups = session.query(Group).options(joinedload(Group.studentinfo)).all()
for i in groups:
    print(vars(i))