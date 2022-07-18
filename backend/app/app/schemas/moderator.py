from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet

from app.schemas.area_of_responsibility import AreaOfResponsibilityGet


class ModeratorBase(BaseModel):
    id: int
    login: str
    password: str
    tel: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[Date]
    location: Optional[LocationGet]
    closed_appeals: Optional[int]
    open_appeals: Optional[int]
    photo: Optional[str]
    area_of_responsibility: Optional[AreaOfResponsibilityGet]  # C
    average_first_response_time: Optional[int]  # или формат должен быть временной
    is_superuser: Optional[bool]


class ModeratorCreate(BaseModel):
    login: str
    password: str
    tel: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[Date]
    location_id: Optional[int]
    closed_appeals: Optional[int]
    open_appeals: Optional[int]
    photo: Optional[str]
    area_of_responsibility_id: Optional[int]  # C
    average_first_response_time: Optional[int]  # или формат должен быть временной
    is_superuser: Optional[bool] = Field(False, title="Этот юзер супер?")


class ModeratorPhoto(BaseModel):
    photo: str = Field(..., title="Фотография")


class ModeratorUpdate(BaseModel):
    pass


class ModeratorGet(BaseModel):
    id: int
    login: str
    password: str
    tel: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[Date]
    location: Optional[LocationGet]
    closed_appeals: Optional[int]
    open_appeals: Optional[int]
    photo: Optional[str]
    area_of_responsibility: Optional[AreaOfResponsibilityGet]  # C
    average_first_response_time: Optional[int]  # или формат должен быть временной
    is_superuser: Optional[bool]

