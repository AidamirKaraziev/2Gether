import datetime
from typing import Optional

from fastapi import Request

from app.schemas import UserBase
from app.core.config import settings, Settings

from app.models import User

from app.getters.location import get_location

from app.utils.time_stamp import to_timestamp

from app.schemas import UserGet


def get_user(user: User, request: Optional[Request], config: Settings = settings) -> UserGet:
    if request is not None:
        url = request.url.hostname + config.API_V1_STR + "/static/"
        if user.photo_main is not None:
            user.photo_main = url + str(user.photo_main)
        if user.photo_1 is not None:
            user.photo_1 = url + str(user.photo_1)
        if user.photo_2 is not None:
            user.photo_2 = url + str(user.photo_2)
    user.birthday = to_timestamp(user.birthday)
    return UserGet(
        id=user.id,
        tel=user.tel,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday,
        location=get_location(user.location) if user.location is not None else None,
        photo_main=user.photo_main,
        photo_1=user.photo_1,
        photo_2=user.photo_2,
        basic_about_me=user.basic_about_me,
        job_title=user.job_title,
        company=user.company,
        about_me=user.about_me,
        contact_phone=user.contact_phone,
        telegram=user.telegram
    )
