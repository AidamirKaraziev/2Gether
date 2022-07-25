import os
import glob
import shutil
import uuid
from typing import Optional

from fastapi import UploadFile, Request
from sqlalchemy import desc
from sqlalchemy.orm import Session
from user_agents import parse

from app.crud.base import CRUDBase
from app.schemas import UserCreate, UserUpdate, DataToCreateUser, UserBasicUpdate
from app.schemas import UserUpdateTel
from app.models.user import User
from app.models import Device, FirebaseToken
from app.exceptions import UnfoundEntity


SECRET_JWT = "AXAS"
DATA_FOLDER = "./static/Photo_users/"


class CrudUser(CRUDBase[User, UserCreate, UserUpdate]):
    def _handle_device(
            self,
            db: Session,
            owner: User,
            host: Optional[str] = None,
            x_real_ip: Optional[str] = None,
            accept_language: Optional[str] = None,
            user_agent: Optional[str] = None,
            x_firebase_token: Optional[str] = None
    ):

        device = db.query(Device).filter(
            Device.user == owner,
            Device.ip_address == host,
            Device.x_real_ip == x_real_ip,
            Device.accept_language == accept_language,
            Device.user_agent == user_agent
        ).order_by(desc(Device.created)).first()

        detected_os = None

        if user_agent is not None:
            ua_string = str(user_agent)
            ua_object = parse(ua_string)

            detected_os = ua_object.os.family
            if detected_os is None or detected_os.lower() == 'other':
                if 'okhttp' in user_agent.lower():
                    detected_os = 'Android'
                elif 'cfnetwork' in user_agent.lower():
                    detected_os = 'iOS'
                else:
                    detected_os = None

        if device is None:
            device = Device()
            device.user = owner
            device.ip_address = host
            device.x_real_ip = x_real_ip
            device.accept_language = accept_language
            device.user_agent = user_agent
            device.detected_os = detected_os
        db.add(device)

        if x_firebase_token is not None:
            firebase_token = FirebaseToken()
            firebase_token.device = device
            firebase_token.value = x_firebase_token
            db.add(firebase_token)

        db.commit()

    def get_by_tel(self, db: Session, *, tel: str) -> Optional[User]:
        return db.query(User).filter(User.tel == tel).first()

    def adding_photo(self, db: Session, num, id_user: int, file: Optional[UploadFile]):
        path_name = DATA_FOLDER + f"{id_user}/{num}/"
        if file is None:
            # Удаляем все содержимое папки
            path_to_clear = path_name + "*"
            for file_to_clear in glob.glob(path_to_clear):
                os.remove(file_to_clear)
            db.query(User).filter(User.id == id_user).update({f'photo_{num}': None})
            db.commit()
            return {f"photo_{num}": None}
        # if file is None:
        #     db.query(User).filter(User.id == id_user).update({f'photo_{num}': None})
        #     db.commit()
        #     return {"photo": None}

        filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        # path_name = DATA_FOLDER + f"{id_user}/{num}/"
        element = ["Photo_users", str(id_user), num, filename]

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

        db.query(User).filter(User.id == id_user).update({f'photo_{num}': path_for_db})
        db.commit()
        if not file:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=2,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body",)
        else:
            return {"photo": path_for_db}

    # Удаляет объект из базы вместе с путем файла
    def remove(self, db: Session, id_user: int):
        path_name = DATA_FOLDER + f"{id_user}"  # сделать константой
        if os.path.exists(path_name):
            shutil.rmtree(path_name)
        return super().remove(db=db, id=id_user)

    def update_tel(self, db: Session, *, db_obj, obj_in: UserUpdateTel):
        db_obj.tel = obj_in.tel
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_user = CrudUser(User)
