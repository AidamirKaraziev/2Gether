from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


from app.models.location import Location


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tel = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    photo_main = Column(String)
    photo_1 = Column(String)
    photo_2 = Column(String)
    basic_about_me = Column(String)  # bref_basic
    job_title = Column(String)
    company = Column(String)
    about_me = Column(String)
    contact_phone = Column(String)
    telegram = Column(String)

    location = relationship(Location)
    # location = relationship(Location, back_populates='users')

    devices = relationship('Device', back_populates='user')

    # Добавить
    # My_project()
