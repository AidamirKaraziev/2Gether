from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from app.models.project import Project

from app.db.base_class import Base

from app.models import PartnerCompetence
from sqlalchemy.orm import relationship


class PartnerCompetenceOfProject(Base):
    __tablename__ = 'partner_competencies_of_project'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id, ondelete="CASCADE"), nullable=False)
    partner_competencies_id = Column(Integer(), ForeignKey(PartnerCompetence.id, ondelete="CASCADE"),  nullable=False)

    project = relationship('Project', back_populates='partner_competencies_of_project')
    partner_competencies = relationship('PartnerCompetence', back_populates='partner_competencies_of_project')

    __table_args__ = (UniqueConstraint('project_id', 'partner_competencies_id'),)
