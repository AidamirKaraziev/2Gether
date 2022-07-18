from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models import Location

from app.models import AreaOfResponsibility


class Moderator(Base):
    __tablename__ = 'moderators'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    tel = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    closed_appeals = Column(Integer)
    open_appeals = Column(Integer)
    photo = Column(String)
    area_of_responsibility_id = Column(Integer, ForeignKey('area_of_responsibility.id', ondelete="SET NULL"))
    average_first_response_time = Column(Integer)
    is_superuser = Column(Boolean, default=False)  # SuperUser

    location = relationship(Location)
    area_of_responsibility = relationship(AreaOfResponsibility)
