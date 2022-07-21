import logging

from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query, Path

from app.core.response import ListOfEntityResponse
from app.crud.crud_location import crud_location

from app.api import deps

from app.core.response import Meta
from app.getters.location import get_location

from app.core.response import SingleEntityResponse
from app.exceptions import UnprocessableEntity
from app.schemas.location import LocationCreate

from app.schemas.location import LocationUpdate

from app.exceptions import UnfoundEntity

router = APIRouter()


# Вывод всех локаций
@router.get('/locations/',
            response_model=ListOfEntityResponse,
            name='Список городов',
            description='Получение списка всех городов',
            tags=['Мобильное приложение / Города']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_location.get_multi(db=session, page=None))

    data, paginator = crud_location.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_location(datum) for datum in data], meta=Meta(paginator=paginator))


# Создание локации
@router.post('/locations/',
             response_model=SingleEntityResponse,
             name='Добавить Город',
             description='Добавить один город в базу данных ',
             tags=['Админ панель / Города']
             )
def create_partner_competence(
        new_data: LocationCreate,
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    obj = crud_location.get_by_name(db=session, name=new_data.name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такой город уже есть в базе данных",
            num=1,
            description="Город с таким названием уже есть в базе данных!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_location(crud_location.create(db=session, obj_in=new_data)))


# Апи удаляет город
@router.delete('/locations/{location_id}/',
               response_model=SingleEntityResponse,
               name='Удалить город',
               description='Полностью удаляет город',
               tags=['Админ панель / Города'])
def delete_location(
        location_id: int = Path(..., title='Id проекта'),
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db)
):
    if crud_location.get(db=session, id=location_id) is None:
        raise UnfoundEntity(
            message="Города с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    return SingleEntityResponse(data=crud_location.remove(db=session, id=location_id))


@router.put('/locations/{location_id}/',
            response_model=SingleEntityResponse,
            name='Изменить название города',
            description='Изменяет название города',
            tags=['Админ панель / Города'])
def update_location(
        name: LocationUpdate,
        location_id: int = Path(..., title='Id проекта'),
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db)
):
    location, code, indexes = crud_location.update_location(db=session, location=name, location_id=location_id)
    if code == -1:
        raise UnfoundEntity(
            message="Города с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Город с таким названием уже есть!",
            num=2,
            description="Выберите другое название города!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_location(db_obj=location))


if __name__ == "__main":
    logging.info('Running...')
