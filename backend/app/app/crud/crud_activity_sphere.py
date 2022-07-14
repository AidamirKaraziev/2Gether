from app.crud.base import CRUDBase
from app.models import ActivitySphere
from app.schemas.activity_sphere import ActivitySphereCreate, ActivitySphereUpdate, ActivitySphereGet


class CrudActivitySphere(CRUDBase[ActivitySphere, ActivitySphereCreate, ActivitySphereUpdate]):  # , ActivitySphereGet
    pass


crud_activity_sphere = CrudActivitySphere(ActivitySphere)
