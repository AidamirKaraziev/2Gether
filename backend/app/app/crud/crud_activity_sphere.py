import os
import shutil
import uuid
from typing import Optional

from app.crud.base import CRUDBase
from app.models import ActivitySphere
from app.schemas.activity_sphere import ActivitySphereCreate, ActivitySphereUpdate, ActivitySphereGet
from fastapi import UploadFile

FOLDER_ACTIVITY_SPHERE = "./static/activity_sphere/"


class CrudActivitySphere(CRUDBase[ActivitySphere, ActivitySphereCreate, ActivitySphereUpdate]):  # , ActivitySphereGet

    # Должно сохранять картинку в папку ./static/activity_sphere/
    def adding_photo(self, file: Optional[UploadFile]):
        # now = datetime.utcnow()
        # year = now.strftime("%Y")
        # month = now.strftime("%m")
        # day = now.strftime("%d")
        # # path_date = f"{year}/{month}/{day}"
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
