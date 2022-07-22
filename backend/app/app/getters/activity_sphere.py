from typing import Optional
from fastapi import Request
from app.models import ActivitySphere
from app.schemas.activity_sphere import ActivitySphereGet

from app.core.config import Settings, settings
from app.schemas.activity_sphere import ActivitySpherePicture


def get_activity_sphere(db_obj: ActivitySphere, request: Optional[Request],
                        config: Settings = settings) -> Optional[ActivitySphereGet]:
    if db_obj.picture is None:
        db_obj.picture = None
    else:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        db_obj.picture = str(url + str(db_obj.picture))
    if request is None:
        return None

    return ActivitySphereGet(
        id=db_obj.id,
        name=db_obj.name,
        picture=db_obj.picture,
    )


def get_picture(path_name: Optional[str], request: Optional[Request],
                config: Settings = settings) -> Optional[ActivitySpherePicture]:
    if path_name is None or request is None:
        return None

    url = request.url.hostname + config.API_V1_STR + "/static/"
    response = str(url + str(path_name))

    return ActivitySpherePicture(
        picture=response,
    )
