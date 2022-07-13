# from datetime import datetime
#
# import sqlalchemy as sa
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     number_phone = sa.Column(sa.Text, unique=True)
#     username = sa.Column(sa.Text, unique=True)
#     password_hash = sa.Column(sa.Text, )
#
#
# class Operations(Base):
#     __tablename__ = 'operations'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
#     date = sa.Column(sa.Date)
#
#
# class VerifCode(Base):
#     __tablename__ = 'verif_code'
#     id = sa.Column(sa.Integer, primary_key=True)
#     value = sa.Column(sa.String, nullable=True)
#     tel = sa.Column(sa.String)
#     created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
#     actual = sa.Column(sa.Boolean, default=True)
#
#
# class UserMy(Base):
#     __tablename__ = 'users'
#     id = sa.Column(sa.Integer, primary_key=True)
#     tel = sa.Column(sa.String, unique=True)
#     first_name = sa.Column(sa.String)
#     last_name = sa.Column(sa.String)
#     birthday = sa.Column(sa.Date)
#     location = sa.Column(sa.String)
#     photo_main = sa.Column(sa.String)
#     photo_1 = sa.Column(sa.String)
#     photo_2 = sa.Column(sa.String)
#     basic_about_me = sa.Column(sa.String)
#     job_title = sa.Column(sa.String)
#     company = sa.Column(sa.String)
#     about_me = sa.Column(sa.String)
#     contact_phone = sa.Column(sa.String)
#     telegram = sa.Column(sa.String)
#     # Добавить
#     # My_project()
#
#
# class Project(Base):
#     __tablename__ = 'projects'
#     id = sa.Column(sa.Integer, primary_key=True)
#     user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
#     name = sa.Column(sa.String)
#     country = sa.Column(sa.String)
#     city = sa.Column(sa.String)
#     business_area = sa.Column(sa.String)  # Выпадающий список
#     stages_of_implementation = sa.Column(sa.String)
#     budget = sa.Column(sa.Integer)
#     partners_share = sa.Column(sa.Integer)  # от 1 до 100
#     Partner_competencies = sa.Column(sa.String)  # Выпадающий список
#     about_the_project = sa.Column(sa.String)
#     site = sa.Column(sa.String)
#     photo_main = sa.Column(sa.String)
#     photo_1 = sa.Column(sa.String)
#     photo_2 = sa.Column(sa.String)
#     photo_3 = sa.Column(sa.String)
#     about_me = sa.Column(sa.String)
#     my_competencies = sa.Column(sa.String)  #
#     opening_hours = sa.Column(sa.Integer)  # часов за неделю
