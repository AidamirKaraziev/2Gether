import datetime
import os
import shutil
import uuid
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Project, User, Location, ActivitySphere, StageOfImplementation, PartnerCompetence
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectGet


DATA_FOLDER_PROJECT = "./static/Photo_project/"


class CrudProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def _check_location(self, db: Session, *, location_id: int):
        return "что-то"

    def _check_activity_sphere(self, db: Session, *, activity_sphere_id_list: List):
        return "что-то"

    def _check_stages_of_implementation(self, db: Session, *, stages_of_implementation_id: int):
        pass

    def _check_partner_competence(self, db: Session, *, partner_competence_id_list: List):
        pass

    def create_project(self, db: Session, *, project: ProjectCreate):  # -> ProjectGet
        # Проверить
        # юзера
        # города
        # сферы деятельности
        # стадии проекта
        # партнерские компетенции
        # найти и добавить в таблицу уже загруженные фотографии(???)

        # Check Id user
        if not (db.query(User).filter(User.id == project.user_id).first()):
            return None, -1, None

        # Check location_id
        if not (db.query(Location).filter(Location.id == project.location).first()):
            return None, -2, None

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
            return None, -3, not_found

        # Check id StageOfImplementation
        if not (db.query(StageOfImplementation).
                filter(StageOfImplementation.id == project.stages_of_implementation).first()):
            return None, -4, None

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
            return None, -5, not_found_competences

        # Создание тут проекта если предыдущие этапы пройдены
        self.create(db=db, obj_in=project)

        # создание тут связей таблиц компетенций и сфер деятельности
        # Смотри crud_story

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


crud_project = CrudProject(Project)
