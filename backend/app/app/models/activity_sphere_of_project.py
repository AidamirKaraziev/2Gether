from sqlalchemy import Column, Integer, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from .activity_sphere import ActivitySphere
from .project import Project

from app.db.base_class import Base


class ActivitySpheresOfProject(Base):
    __tablename__ = 'activity_spheres_of_project'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id, ondelete="CASCADE"),  nullable=False)
    activity_of_sphere_id = Column(Integer, ForeignKey(ActivitySphere.id, ondelete="CASCADE"),  nullable=False)

    project = relationship('Project', back_populates='activity_spheres_of_project')

    activity_spheres = relationship('ActivitySphere', back_populates='activity_spheres_of_project')

    __table_args__ = (UniqueConstraint('project_id', 'activity_of_sphere_id'),)
