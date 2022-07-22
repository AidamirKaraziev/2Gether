import datetime
import time

import hashlib
import os
from typing import Optional
from fastapi import Request

from app.getters.area_of_responsibility import get_area_of_responsibility
from app.getters.location import get_location
from app.models.moderator import Moderator

from app.schemas.moderator import ModeratorGet

from app.schemas.moderator import ModeratorCreate, ModeratorRequest

from app.core.config import Settings, settings

from app.utils.time_stamp import to_timestamp

# def get_moderator(moderator: Moderator) -> Optional[ModeratorGet]:
#     return ModeratorGet(
#         id=moderator.id,
#         login=moderator.login,
#         tel=moderator.tel,
#         first_name=moderator.first_name,
#         last_name=moderator.last_name,
#         birthday=moderator.birthday,
#         location=get_location(moderator.location) if moderator.location is not None else None,
#         photo=moderator.photo,
#         area_of_responsibility=get_area_of_responsibility(
#             moderator.area_of_responsibility) if moderator.area_of_responsibility is not None else None,
#         average_first_response_time=moderator.average_first_response_time,
#         is_superuser=moderator.is_superuser
#     )
from app.schemas.moderator import ModeratorGetDelete


def get_moderator(moderator: Moderator, request: Optional[Request],
                  config: Settings = settings) -> Optional[ModeratorGet]:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if moderator.photo is not None:
            moderator.photo = url + str(moderator.photo)
        else:
            moderator.photo = None
    moderator.birthday = to_timestamp(moderator.birthday)
    return ModeratorGet(
        id=moderator.id,
        login=moderator.login,
        tel=moderator.tel,
        first_name=moderator.first_name,
        last_name=moderator.last_name,
        birthday=moderator.birthday,
        location=get_location(moderator.location) if moderator.location is not None else None,
        photo=moderator.photo,
        area_of_responsibility=get_area_of_responsibility(
            moderator.area_of_responsibility) if moderator.area_of_responsibility is not None else None,
        average_first_response_time=moderator.average_first_response_time,
        is_superuser=moderator.is_superuser
    )


def get_moderator_delete(moderator: Moderator, request: Optional[Request],
                         config: Settings = settings) -> Optional[ModeratorGetDelete]:
    moderator.birthday = to_timestamp(moderator.birthday)
    return ModeratorGetDelete(
        id=moderator.id,
        login=moderator.login,
        tel=moderator.tel,
        first_name=moderator.first_name,
        last_name=moderator.last_name,
        birthday=moderator.birthday,
        location=moderator.location_id,
        photo=moderator.photo,
        area_of_responsibility=moderator.area_of_responsibility_id,
        average_first_response_time=moderator.average_first_response_time,
        is_superuser=moderator.is_superuser
    )


def get_moderator_for_create(moderator: ModeratorRequest) -> ModeratorCreate:
    # salt = os.urandom(32)  # Запомните
    # password = moderator.password
    #
    # key = hashlib.pbkdf2_hmac(
    #     'sha256',  # Используемый алгоритм хеширования
    #     password.encode('utf-8'),  # Конвертируется пароль в байты
    #     salt,  # Предоставляется соль
    #     100000)  # Рекомендуется использовать хотя бы 100000 итераций SHA-256
    return ModeratorCreate(
        login=moderator.login,

        # password=moderator.password,
        tel=moderator.tel,
        first_name=moderator.first_name,
        last_name=moderator.last_name,
        birthday=moderator.birthday,
        location=moderator.location_id,
        closed_appeals=moderator.closed_appeals,
        open_appeals=moderator.open_appeals,
        photo=moderator.photo,
        area_of_responsibility=moderator.area_of_responsibility_id,
        average_first_response_time=moderator.average_first_response_time,
        is_superuser=moderator.is_superuser
    )