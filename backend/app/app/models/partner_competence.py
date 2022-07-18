from sqlalchemy import Column, String, Integer
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class PartnerCompetence(Base):
    __tablename__ = 'partner_competencies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # как я понял
    partner_competencies_of_project = relationship('PartnerCompetenceOfProject',
                                                   back_populates='partner_competencies', cascade="all, delete")
