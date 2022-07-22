from typing import Optional
from fastapi import Request, Depends

from app.core.config import settings, Settings

from app.models import Project

from app.schemas.project import ProjectGet
from app.schemas.project import ProjectCreate
from app.schemas.project import ProjectPhoto
from app.schemas.project import ProjectForCreateInDB

from app.getters.location import get_location
from app.getters.stage_of_implementation import get_stage_of_implementation
from app.getters.activity_sphere import get_activity_sphere
from app.getters.partner_competence import get_partner_competence


# Геттерс для фронта
def get_project(project: Optional[Project], request: Request) -> Optional[ProjectGet]:
    return ProjectGet(
        id=project.id,
        user_id=project.user_id,  # Когда выводим user_id нужно ли выводить данные пользователя?
        name=project.name,
        location_id=get_location(project.location) if project.location is not None else None,
        activity_spheres_of_project=[
            get_activity_sphere(aop.activity_spheres, request=request) for aop in project.activity_spheres_of_project
        ],
        stages_of_implementation_id=get_stage_of_implementation(
            project.stages_of_implementation) if project.stages_of_implementation is not None else None,
        budget=project.budget,
        partners_share=project.partners_share,
        partner_competencies_of_project=[
                    get_partner_competence(cop.partner_competencies) for cop in project.partner_competencies_of_project
                ],
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


def get_project_photo(path_name: Optional[str], request: Optional[Request],
                      config: Settings = settings) -> Optional[ProjectPhoto]:
    if path_name is None or request is None:
        return None

    url = request.url.hostname + config.API_V1_STR + "/static/"
    response = str(url + str(path_name))

    return ProjectPhoto(
        photo=response,
    )


# Геттерс который отдает для базы данных готовый вариант для создания
def get_project_for_db(user_id: int, project: ProjectCreate) -> Optional[ProjectForCreateInDB]:
    return ProjectForCreateInDB(
        user_id=user_id,
        name=project.name,
        location_id=project.location_id,
        stages_of_implementation_id=project.stages_of_implementation_id,
        budget=project.budget,
        partners_share=project.partners_share,
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


def get_for_delete(project: Optional[Project]) -> Optional[ProjectCreate]:
    return ProjectCreate(
        user_id=project.user_id,
        name=project.name,
        location_id=project.location_id,
        stages_of_implementation_id=project.stages_of_implementation_id,
        budget=project.budget,
        partners_share=project.partners_share,
        about_the_project=project.about_the_project,
        site=project.site,
        photo_main=project.photo_main,
        photo_1=project.photo_1,
        photo_2=project.photo_2,
        about_me=project.about_me,
        work_experience=project.work_experience,
        my_strengths=project.my_strengths,
        opening_hours=project.opening_hours)