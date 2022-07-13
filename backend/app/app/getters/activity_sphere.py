from app.models import ActivitySphere
from app.schemas.activity_sphere import ActivitySphereGet


def get_activity_sphere(db_obj: ActivitySphere) -> ActivitySphereGet:
    return ActivitySphereGet(
        id=db_obj.id,
        name=db_obj.name,
        picture=db_obj.picture,
    )
