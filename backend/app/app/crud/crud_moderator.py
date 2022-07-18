import glob
import os
import shutil
import uuid
from typing import Optional

from app.crud.base import CRUDBase
from app.models.moderator import Moderator
from app.schemas.moderator import ModeratorCreate, ModeratorUpdate
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.exceptions import UnfoundEntity

FOLDER_MODERATOR_PHOTO = './static/Moderator_photo/'


class CrudModerator(CRUDBase[Moderator, ModeratorCreate, ModeratorUpdate]):
    def get_by_login(self, db: Session, *, login: str):
        return db.query(self.model).filter(self.model.login == login).first()

    def adding_photo(self, db: Session, num, id_moderator: int, file: Optional[UploadFile]):

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        path_name = FOLDER_MODERATOR_PHOTO + f"{id_moderator}/"
        element = ["Moderator_photo", str(id_moderator), filename]

        path_for_db = "/".join(element)

        if not os.path.exists(path_name):
            os.makedirs(path_name)

        # Удаляем все содержимое папки
        path_to_clear = path_name + "*"
        for file_to_clear in glob.glob(path_to_clear):
            os.remove(file_to_clear)

        with open(path_name + filename, "wb") as wf:
            shutil.copyfileobj(file.file, wf)
            file.file.close()  # удаляет временный

        db.query(Moderator).filter(Moderator.id == id_moderator).update({f'photo': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=2,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body", )
        else:
            return {"photo": path_for_db}


crud_moderator = CrudModerator(Moderator)
