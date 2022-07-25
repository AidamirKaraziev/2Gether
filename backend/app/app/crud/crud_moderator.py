import hashlib
import os
import glob
import os
import shutil
import uuid
from typing import Optional, Any, Union, Dict

from app.crud.base import CRUDBase
from app.models.moderator import Moderator
from app.schemas.moderator import ModeratorCreate, ModeratorUpdate
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.exceptions import UnfoundEntity

from app.schemas.moderator import ModeratorEntrance

from app.crud.base import ModelType

from app.core.security import verify_password
from app.exceptions import UnprocessableEntity

from app.schemas.moderator import ModeratorRequest

from app.models import Location, AreaOfResponsibility

from app.core.security import get_password_hash
from app.utils.time_stamp import date_from_timestamp

from app.crud.area_of_responsibility import crud_area_of_responsibility
from app.crud.crud_location import crud_location

FOLDER_MODERATOR_PHOTO = './static/Moderator_photo/'


class CrudModerator(CRUDBase[Moderator, ModeratorCreate, ModeratorUpdate]):
    def get_moderator(self, db: Session, *, moderator: ModeratorEntrance):
        getting_moderator = db.query(Moderator).filter(Moderator.login == moderator.login).first()
        if getting_moderator is None or \
                not verify_password(plain_password=moderator.password, hashed_password=getting_moderator.password):
            raise UnprocessableEntity(
                message="Неверный логин или пароль",
                num=1,
                description="Неверный логи или пароль",
                path="$.body"
            )
        return getting_moderator

    def get_by_login(self, db: Session, *, login: str):
        return db.query(Moderator).filter(Moderator.login == login).first()

    # def get_admin(self,  db: Session, *, moderator: ModeratorEntrance):
    #     return db.query(self.model).filter(self.model.login == moderator.login,
    #                                        self.model.password == moderator.password).first()

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(Moderator).filter(Moderator.id == id).first()

    def adding_photo(self, db: Session, id_moderator: int, file: Optional[UploadFile]):
        path_name = FOLDER_MODERATOR_PHOTO + f"{id_moderator}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(Moderator).filter(Moderator.id == id_moderator).update({f'photo': None})
            db.commit()
            return {"photo": None}
        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = FOLDER_MODERATOR_PHOTO + f"{id_moderator}/"
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

    # Проверяет, является ли superuser
    def check_is_superuser(self, db: Session, *, current_moderator: Moderator):
        db_obj = crud_moderator.get(db=db, id=current_moderator.id)
        # Проверить есть ли такой модератор
        if db_obj is None:
            return None, -1, None
        # Проверить является ли is_superuser
        if current_moderator.is_superuser is False:
            return None, -2, None
        return db_obj, 0, None

    def update_moderator_self(self, db: Session, *, current_moderator: Moderator,
                              obj_in: Union[ModeratorRequest, Dict[str, Any]]) -> Moderator:
        db_obj = crud_moderator.get(db=db, id=current_moderator.id)
        obj_data = jsonable_encoder(db_obj)
        new_obj = jsonable_encoder(obj_in)
        # Проверить есть ли такой модератор
        if db_obj is None:
            return None, -1, None
        # Проверить является ли is_superuser
        if current_moderator.is_superuser:
            # ГОРОДА
            if new_obj['location_id'] is not None:
                if crud_location.get(db=db, id=new_obj['location_id']) is None:
                    return None, -2, None
            # ЗОНЫ ОТВЕТСТВЕННОСТИ
            if new_obj["area_of_responsibility_id"] is not None:
                if crud_area_of_responsibility.get(db=db, id=new_obj["area_of_responsibility_id"]) is None:
                    return None, -3, None
        else:
            # Проверить доступ к админству
            if obj_in.is_superuser is True:
                return None, -4, None
            # Проверить доступ к зонам ответственности
            if obj_in.area_of_responsibility_id is not None:
                return None, -5, None
            # ГОРОДА
            if new_obj['location_id'] is not None:
                if crud_location.get(db=db, id=new_obj['location_id']) is None:
                    return None, -2, None
        if new_obj['password'] is not None:
            psw = get_password_hash(password=new_obj["password"])
            obj_in.password = psw
        if new_obj['birthday'] is not None:
            obj_in.birthday = str(date_from_timestamp(new_obj['birthday']))

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def update_moderator(self, db: Session, *, moderator_id: int, current_moderator: Moderator,
                         obj_in: Union[ModeratorRequest, Dict[str, Any]]) -> Moderator:
        # Проверить является ли is_superuser
        if not current_moderator.is_superuser:
            return None, -1, None
        # Check id
        db_obj = db.query(Moderator).filter(Moderator.id == moderator_id).first()
        if db_obj is None:
            return None, -2, None

        obj_data = jsonable_encoder(db_obj)
        in_ob = jsonable_encoder(obj_in)
        # Check Location
        if in_ob['location_id'] is not None:
            if not (db.query(Location).filter(Location.id == in_ob['location_id']).first()):
                return None, -3, None
        # Check responsibility areas
        if in_ob['area_of_responsibility_id'] is not None:
            if not (db.query(AreaOfResponsibility).filter(
                    AreaOfResponsibility.id == in_ob['area_of_responsibility_id']).first()):
                return None, -4, None
        if in_ob['password'] is not None:
            psw = get_password_hash(password=in_ob["password"])
            obj_in.password = psw
        if in_ob['birthday'] is not None:
            obj_in.birthday = str(date_from_timestamp(in_ob['birthday']))

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None


crud_moderator = CrudModerator(Moderator)
