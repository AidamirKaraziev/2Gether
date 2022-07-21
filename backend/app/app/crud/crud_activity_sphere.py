import os
import shutil
import uuid
from typing import Optional

from app.crud.base import CRUDBase
from app.models import ActivitySphere
from app.schemas.activity_sphere import ActivitySphereCreate, ActivitySphereUpdate, ActivitySphereGet
from fastapi import UploadFile
from sqlalchemy.orm import Session

FOLDER_ACTIVITY_SPHERE = "./static/activity_sphere/"


class CrudActivitySphere(CRUDBase[ActivitySphere, ActivitySphereCreate, ActivitySphereUpdate]):  # , ActivitySphereGet
    def update_activity_spheres(self, db: Session, *, new_data: Optional[ActivitySphereUpdate],
                        id: int):
        # проверить есть ли сфера с таким id
        this_object = (db.query(
            ActivitySphere).filter(ActivitySphere.id == id).first())
        if this_object is None:
            return None, -1, None

        # Check_name
        if this_object.name != new_data.name:
            if db.query(ActivitySphere).filter(ActivitySphere.name == new_data.name).first() is not None:
                return None, -2, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_object, obj_in=new_data)
        return db_obj, 0, None



    # Должно сохранять картинку в папку ./static/activity_sphere/
    def adding_photo(self, file: Optional[UploadFile]):
        path_name = FOLDER_ACTIVITY_SPHERE

        if file is None:
            return None

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        element = ["activity_sphere", filename]

        path_for_url = "/".join(element)

        if not os.path.exists(path_name):
            os.makedirs(path_name)

        with open(path_name + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        return path_for_url


crud_activity_sphere = CrudActivitySphere(ActivitySphere)
