import logging

from fastapi import APIRouter, Depends, Query, Path

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.area_of_responsibility import crud_area_of_responsibility
from app.getters.area_of_responsibility import get_area_of_responsibility

from app.core.response import SingleEntityResponse
from app.exceptions import UnprocessableEntity
from app.schemas.area_of_responsibility import AreaOfResponsibilityCreate

from app.exceptions import UnfoundEntity

from app.schemas.area_of_responsibility import AreaOfResponsibilityUpdate

router = APIRouter()


# GET ALL
@router.get('/responsibility-areas/',
            response_model=ListOfEntityResponse,
            name='Список зон ответственности',
            description='Получение списка всех зон ответственности',
            tags=['Мобильное приложение / Зоны ответственности']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_area_of_responsibility.get_multi(db=session, page=None))

    data, paginator = crud_area_of_responsibility.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_area_of_responsibility(datum) for datum in data], meta=Meta(paginator=paginator))


# CREATE
@router.post('/responsibility-areas/',
             response_model=SingleEntityResponse,
             name='Создать зону ответственности',
             description='Создать зону ответственности',
             tags=['Админ панель / Зоны ответственности']
             )
def create_responsibility_area(
        new_data: AreaOfResponsibilityCreate,
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    obj = crud_area_of_responsibility.get_by_name(db=session, name=new_data.name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такая компетенция уже есть",
            num=1,
            description="Компетенция с таким названием уже есть!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_area_of_responsibility(
        crud_area_of_responsibility.create(db=session, obj_in=new_data)))


# UPDATE
@router.put('/responsibility-areas/{responsibility_area_id}/',
            response_model=SingleEntityResponse,
            name='Изменить зону ответственности',
            description='Изменяет название зоны ответственности',
            tags=['Админ панель / Зоны ответственности'])
def update_responsibility_area(
        name: AreaOfResponsibilityUpdate,
        responsibility_area_id: int = Path(..., title='Id зоны ответственности'),
        session=Depends(deps.get_db)
):
    responsibility_area, code, indexes = crud_area_of_responsibility.update_responsibility_area(
        db=session, new_data=name, id=responsibility_area_id)
    if code == -1:
        raise UnfoundEntity(
            message="Зоны ответственности с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Зона ответственности с таким названием уже есть!",
            num=2,
            description="Выберите другое название зоны ответственности!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_area_of_responsibility(db_obj=responsibility_area))


# DELETE
@router.delete('/responsibility-areas/{responsibility_area_id}/',
               response_model=SingleEntityResponse,
               name='Удалить зону ответственности',
               description='Полностью удаляет зону ответственности',
               tags=['Админ панель / Зоны ответственности'])
def delete_responsibility_area(
        responsibility_area_id: int = Path(..., title='Id Зоны ответственности'),
        session=Depends(deps.get_db)
):
    if crud_area_of_responsibility.get(db=session, id=responsibility_area_id) is None:
        raise UnfoundEntity(
            message="Зоны ответственности с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    return SingleEntityResponse(data=crud_area_of_responsibility.remove(db=session, id=responsibility_area_id))


if __name__ == "__main":
    logging.info('Running...')
