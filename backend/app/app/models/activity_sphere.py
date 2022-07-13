from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ActivitySphere(Base):
    __tablename__ = 'activity_spheres'
    id = Column(Integer, primary_key=True)  #
    name = Column(String, unique=True)  # название сферы деятельности
    picture = Column(String)  # Картинка на сферу деятельности

    activity_spheres_of_project = relationship('ActivitySpheresOfProject',
                                               back_populates='activity_spheres', cascade="all, delete")
