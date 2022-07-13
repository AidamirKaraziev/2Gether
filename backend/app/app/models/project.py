from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Table

from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models import Location
from app.models.stage_of_implementation import StageOfImplementation


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)

    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))  # City
    stages_of_implementation_id = Column(Integer, ForeignKey("stage_of_implementation.id", ondelete="SET NULL"))
    budget = Column(Integer)
    partners_share = Column(Integer)  # от 1 до 100 ДОЛЯ ПАРТНЕРА

    about_the_project = Column(String)
    site = Column(String)
    photo_main = Column(String)
    photo_1 = Column(String)
    photo_2 = Column(String)
    about_me = Column(String)
    work_experience = Column(String)
    my_strengths = Column(String)  # Это текст
    opening_hours = Column(Integer)  # часов за неделю готов уделять

    location = relationship(Location)
    stages_of_implementation = relationship(StageOfImplementation)

    #
    activity_spheres_of_project = relationship('ActivitySpheresOfProject',
                                               back_populates='project', cascade="all, delete")
    partner_competencies_of_project = relationship('PartnerCompetenceOfProject',
                                                   back_populates='project', cascade="all, delete")

# Вопрос:
# Надо убрать повторения в базе данных(уникальное значение по двум столбцам)
# Надо убрать чтобы, чтобы null был в связочной таблице
#
