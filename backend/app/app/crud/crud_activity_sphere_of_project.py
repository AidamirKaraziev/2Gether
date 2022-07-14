from app.crud.base import CRUDBase

from app.models import ActivitySpheresOfProject
from app.schemas.activity_sphere_of_project import ActivitySphereOfProjectCreate, ActivitySphereOfProjectUpdate


class CrudActivitySphereOfProject(CRUDBase[ActivitySpheresOfProject, ActivitySphereOfProjectCreate,
                                           ActivitySphereOfProjectUpdate]):

    pass


crud_activity_sphere_of_project = CrudActivitySphereOfProject(ActivitySpheresOfProject)
