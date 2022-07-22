from typing import Optional, List

from pydantic import BaseModel, Field

from app.schemas.location import LocationGet
from app.schemas.stage_of_implementation import StageOfImplementationGet


class ProjectBase(BaseModel):
    id: int
    user_id: int
    name: Optional[str]
    location_id: Optional[LocationGet]
    activity_spheres_of_project: Optional[List]
    stages_of_implementation_id: Optional[int]
    budget: Optional[int]
    partners_share: Optional[int]
    partner_competencies_of_project: Optional[List]
    about_the_project: Optional[str]
    site: Optional[str]
    photo_main: Optional[str]
    photo_1: Optional[str]
    photo_2: Optional[str]
    about_me: Optional[str]
    work_experience: Optional[str]
    my_strengths: Optional[str]
    opening_hours: Optional[int]


class ProjectCreate(BaseModel):  # это будет запрашиваемая информация для создания проекта
    # user_id: int = Field(None, title="id пользователя")  # надо ли проверять есть ли такой юзер?
    # user_id будет прилетать в токене
    name: Optional[str] = Field(None, title="Название")
    location_id: Optional[int] = Field(title="id города")
    activity_spheres: Optional[List[int]] = Field(None, title="Список id сфер деятельности")
    stages_of_implementation_id: Optional[int] = Field( title="id стадии реализации")
    budget: Optional[int] = Field(None, title="Бюджет")
    partners_share: Optional[int] = Field(None, title="Доля партнера")
    partner_competences: Optional[List[int]] = Field(None, title="Компетенции партнера список id")
    about_the_project: Optional[str] = Field(None, title="О проекте")
    site: Optional[str] = Field(None, title="Сайт")
    photo_main: Optional[str] = Field(None, title="Главная фотка")
    photo_1: Optional[str] = Field(None, title="Фото 1")
    photo_2: Optional[str] = Field(None, title="Фото 2")
    about_me: Optional[str] = Field(None, title="Обо мне")
    work_experience: Optional[str] = Field(None, title="Опыт работы")
    my_strengths: Optional[str] = Field(None, title="Мои сильные стороны")
    opening_hours: Optional[int] = Field(None, title="Часов в неделю готов уделять")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Название")
    location_id: Optional[int] = Field(title="id города")
    activity_spheres: Optional[List[int]] = Field(None, title="Список id сфер деятельности")
    stages_of_implementation_id: Optional[int] = Field(title="id стадии реализации")
    budget: Optional[int] = Field(None, title="Бюджет")
    partners_share: Optional[int] = Field(None, title="Доля партнера")
    partner_competences: Optional[List[int]] = Field(None, title="Компетенции партнера список id")
    about_the_project: Optional[str] = Field(None, title="О проекте")
    site: Optional[str] = Field(None, title="Сайт")
    photo_main: Optional[str] = Field(None, title="Главная фотка")
    photo_1: Optional[str] = Field(None, title="Фото 1")
    photo_2: Optional[str] = Field(None, title="Фото 2")
    about_me: Optional[str] = Field(None, title="Обо мне")
    work_experience: Optional[str] = Field(None, title="Опыт работы")
    my_strengths: Optional[str] = Field(None, title="Мои сильные стороны")
    opening_hours: Optional[int] = Field(None, title="Часов в неделю готов уделять")


class ProjectForCreateInDB(BaseModel):
    user_id: int = Field(None, title="id пользователя")
    name: Optional[str] = Field(None, title="Название")
    location_id: Optional[int] = Field(title="id города")
    stages_of_implementation_id: Optional[int] = Field(title="id стадии реализации")
    budget: Optional[int] = Field(None, title="Бюджет")
    partners_share: Optional[int] = Field(None, title="Доля партнера")
    about_the_project: Optional[str] = Field(None, title="О проекте")
    site: Optional[str] = Field(None, title="Сайт")
    photo_main: Optional[str] = Field(None, title="Главная фотка")
    photo_1: Optional[str] = Field(None, title="Фото 1")
    photo_2: Optional[str] = Field(None, title="Фото 2")
    about_me: Optional[str] = Field(None, title="Обо мне")
    work_experience: Optional[str] = Field(None, title="Опыт работы")
    my_strengths: Optional[str] = Field(None, title="Мои сильные стороны")
    opening_hours: Optional[int] = Field(None, title="Часов в неделю готов уделять")


class ProjectGet(BaseModel):
    id: int
    user_id: int
    name: Optional[str]
    location_id: Optional[LocationGet]
    activity_spheres_of_project: Optional[List]  # ActivitySphereOfProjectGet
    stages_of_implementation_id: Optional[StageOfImplementationGet]  # StageOfImplementationGet
    budget: Optional[int]
    partners_share: Optional[int]
    partner_competencies_of_project: Optional[List]  # PartnerCompetenceOfProjectGet
    about_the_project: Optional[str]
    site: Optional[str]
    photo_main: Optional[str]
    photo_1: Optional[str]
    photo_2: Optional[str]
    about_me: Optional[str]
    work_experience: Optional[str]
    my_strengths: Optional[str]
    opening_hours: Optional[int]


class ProjectPhoto(BaseModel):
    photo: Optional[str]
