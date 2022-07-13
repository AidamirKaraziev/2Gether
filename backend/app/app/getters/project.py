from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings
from app.getters.location import get_location
from app.models import Project
from app.schemas.project import ProjectGet

from app.schemas.project import ProjectPhoto
from app.core.config import settings, Settings



def get_project(project: Project, config: Settings = settings) -> ProjectGet:  #  request: Optional[Request],
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if user.photo_main is not None:
            user.photo_main = url + str(user.photo_main)
        if user.photo_1 is not None:
            user.photo_1 = url + str(user.photo_1)
        if user.photo_2 is not None:
            user.photo_2 = url + str(user.photo_2)
    return ProjectGet(
        id=project.id,
        user_id=project.user_id,  # Когда выводим user_id нужно ли выводить данные пользователя
        name=project.name,
        location=get_location(project.location_id) if project.location is not None else None,
        activity_spheres_of_project=get_activity_sphere_of_project(),

        photo_main=project.photo_main,
        photo_1=project.photo_1,
        photo_2=project.photo_2,

    )


def get_project_photo(project: ProjectPhoto, request: Optional[Request],):
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if user.photo_main is not None:
            user.photo_main = url + str(user.photo_main)
        if user.photo_1 is not None:
            user.photo_1 = url + str(user.photo_1)
        if user.photo_2 is not None:
            user.photo_2 = url + str(user.photo_2)