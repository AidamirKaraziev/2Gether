from typing import Optional
from fastapi import Request

from app.core.config import Settings, settings
from app.getters.location import get_location
from app.models import Project
from app.schemas.project import ProjectGet

from app.schemas.project import ProjectPhoto
from app.core.config import settings, Settings


def get_project(project: Project, request: Optional[Request], config: Settings = settings) -> ProjectGet:  #
    return ProjectGet(
        id=project.id,
        user_id=project.user_id,  # Когда выводим user_id нужно ли выводить данные пользователя
        name=project.name,
        location=get_location(project.location_id) if project.location is not None else None,
        activity_spheres_of_project=[
            get_activity_sphere(aop.activity_spheres) for aop in project.activity_spheres_of_project
        ],
        stages_of_implementation=get_stage_of_implementation(
            project.stages_of_implementation_id) if project.stages_of_implementation is not None else None,
        budget=project.budget,
        partners_share=project.partners_share,
        partner_competencies_of_project=get_partner_competence_of_project(),
        about_the_project=project.about_the_project,
        site=project.site,
        photo_main=project.photo_main,
        photo_1=project.photo_1,
        photo_2=project.photo_2,
        about_me=project.about_me,
        work_experience=project.work_experience,
        my_strengths=project.my_strengths,
        opening_hours=project.opening_hours
    )


def get_project_photo(path_name: Optional[str], request: Optional[Request], config: Settings = settings) -> Optional[ProjectPhoto]:
    if path_name is None or request is None:
        return None

    url = request.url.hostname + config.API_V1_STR + "/static/"
    response = str(url + str(path_name))

    return ProjectPhoto(
        photo=response,
    )