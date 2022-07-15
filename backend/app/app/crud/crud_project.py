import datetime
import os
import shutil
import uuid
from typing import List, Optional, Any, Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Project, User, Location, ActivitySphere, StageOfImplementation, PartnerCompetence
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectGet

from app.getters.project import get_project_for_db

from app.schemas.partner_competence_of_project import PartnerCompetenceOfProjectCreate

from app.crud.partner_competence_of_project import crud_partner_competence_of_project

from app.crud.crud_activity_sphere_of_project import crud_activity_sphere_of_project
from app.schemas.activity_sphere_of_project import ActivitySphereOfProjectCreate

from app.models import ActivitySpheresOfProject, PartnerCompetenceOfProject

from app.core.response import Paginator
from app.crud.base import ModelType
from app.utils import pagination

from app.exceptions import UnfoundEntity

DATA_FOLDER_PROJECT = "./static/Photo_project/"


class CrudProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_project(self, db: Session, *, project: ProjectCreate, user_id: int):  # -> ProjectGet

        # Check name
        if (db.query(Project).filter(Project.name == project.name).first()) is not None:
            return None, -1, None

        # Check Id user
        if not (db.query(User).filter(User.id == user_id).first()):
            return None, -2, None

        # Check location
        if not (db.query(Location).filter(Location.id == project.location_id).first()):
            return None, -3, None

        # Check id activity_sphere
        not_found = []
        activity_spheres = []
        for num, activity_id in enumerate(project.activity_spheres):
            activity_sphere = (db.query(ActivitySphere).filter(ActivitySphere.id == activity_id).first())
            if activity_sphere is None:
                not_found.append(num)
            else:
                activity_spheres.append(activity_sphere)
        if len(not_found) > 0:
            return None, -4, not_found

        # Check id StageOfImplementation
        if not (db.query(StageOfImplementation).
                filter(StageOfImplementation.id == project.stages_of_implementation_id).first()):
            return None, -5, None

        # Check id PartnerCompetence
        not_found_competences = []
        partner_competences = []
        for num, competence_id in enumerate(project.partner_competences):
            partner_competence = (db.query(PartnerCompetence).filter(PartnerCompetence.id == competence_id).first())
            if partner_competence is None:
                not_found_competences.append(num)
            else:
                partner_competences.append(partner_competence)
        if len(not_found_competences) > 0:
            return None, -6, not_found_competences

        # Создание тут проекта если предыдущие этапы пройдены
        db_project = get_project_for_db(user_id=user_id, project=project)
        db_obj = super().create(db=db, obj_in=db_project)
        db_obj = db.query(Project).filter(Project.user_id == user_id, Project.name == db_obj.name).first()
        project_id = db_obj.id
        # создание тут связей таблиц компетенций и сфер деятельности
        if partner_competences is not None:
            for partner_competence in partner_competences:
                competence_project = PartnerCompetenceOfProjectCreate(project_id=project_id,
                                                                      partner_competencies_id=partner_competence.id)
                crud_partner_competence_of_project.create(db=db, obj_in=competence_project)
        if activity_spheres is not None:
            for activity_sphere in activity_spheres:
                activity_sphere_project = ActivitySphereOfProjectCreate(project_id=project_id,
                                                                        activity_of_sphere_id=activity_sphere.id)
                crud_activity_sphere_of_project.create(db=db, obj_in=activity_sphere_project)
        # Смотри crud_story
        db.query(ActivitySpheresOfProject).filter(ActivitySpheresOfProject.project_id == project_id).all()
        db.query(PartnerCompetenceOfProject).filter(PartnerCompetenceOfProject.project_id == project_id).all()

        return db_obj, 0, None

    # Должно сохранять фото год, месяц, день,
    def adding_photo(self, file: Optional[UploadFile]):
        now = datetime.datetime.utcnow()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        path_date = f"{year}/{month}/{day}"
        path_name = DATA_FOLDER_PROJECT + path_date + "/"

        if file is None:
            return None

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        element = ["Photo_project", path_date, filename]

        path_for_url = "/".join(element)

        if not os.path.exists(path_name):
            os.makedirs(path_name)

        with open(path_name + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        return path_for_url

    # Хуня какая-то
    # def get_multi_project(
    #         self, db: Session, *, page: Optional[int] = None, user_id: int
    # ) -> Tuple[List[ModelType], Paginator]:
    #     query = db.query(self.model.id).filter(self.model.user_id == user_id)
    #     query_id = []
    #     for quer in query:
    #         query_id.append(quer.id)
    #     return pagination.get_page(query, page)

    def get_multi_project(self, db: Session, *, user_id: int):
        requests = db.query(Project).filter(Project.user_id == user_id)
        query_id = []
        for query in requests:
            query_id.append(query.id)
        if not query_id:
            raise UnfoundEntity(message="Нет проектов",
                                num=1,
                                description="Нет проектов",
                                path="$.body",
                                )
        return query_id

    def get_by_name(self, db: Session, name: str):
        return db.query(self.model).filter(self.model.name == name).first()

    def getting(self, db: Session, user_id: int, project_id: int):
        return db.query(self.model).filter(self.model.user_id == user_id, self.model.id == project_id).first()

    def update_project(self, db: Session, *, project: Optional[ProjectCreate], user_id: int, project_id: int):

        this_project = (db.query(Project).filter(Project.id == project_id).first())

        # Check name
        if this_project.name != project.name:
            if (db.query(Project).filter(Project.name == project.name).first()) is not None:
                return None, -1, None
        # Check Id user
        if not (db.query(User).filter(User.id == user_id).first()):
            return None, -2, None

        # Check belonging user_id -- project_id
        if (db.query(Project).filter(Project.user_id == user_id, Project.id == project_id).first()) is None:
            return None, -3, None

        # Check location
        if project.location_id in project:
            if not (db.query(Location).filter(Location.id == project.location_id).first()):
                return None, -4, None

        # Check id activity_sphere
        if project.activity_spheres in project:
            not_found = []
            activity_spheres = []
            for num, activity_id in enumerate(project.activity_spheres):
                activity_sphere = (db.query(ActivitySphere).filter(ActivitySphere.id == activity_id).first())
                if activity_sphere is None:
                    not_found.append(num)
                else:
                    activity_spheres.append(activity_sphere)
            if len(not_found) > 0:
                return None, -5, not_found

        # Check id StageOfImplementation
        if project.stages_of_implementation_id in project:
            if not (db.query(StageOfImplementation).
                    filter(StageOfImplementation.id == project.stages_of_implementation_id).first()):
                return None, -6, None

        # Check id PartnerCompetence
        if project.partner_competences in project:
            not_found_competences = []
            partner_competences = []
            for num, competence_id in enumerate(project.partner_competences):
                partner_competence = (db.query(PartnerCompetence).filter(PartnerCompetence.id == competence_id).first())
                if partner_competence is None:
                    not_found_competences.append(num)
                else:
                    partner_competences.append(partner_competence)
            if len(not_found_competences) > 0:
                return None, -7, not_found_competences
        # Вот тут должно быть обновление базы данных
        db_obj = (db.query(Project).filter(Project.id == project_id).first())
        db_obj = super().update(db=db, db_obj=db_obj, obj_in=project)
        return db_obj, 0, None


crud_project = CrudProject(Project)
