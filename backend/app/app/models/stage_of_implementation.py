from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class StageOfImplementation(Base):
    __tablename__ = 'stage_of_implementation'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
