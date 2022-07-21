import logging

from fastapi import APIRouter, Depends, Query, Path

from app.core.response import ListOfEntityResponse
from app.crud.crud_partner_competence import crud_partner_competence
from app.getters.partner_competence import get_partner_competence

from app.api import deps

from app.core.response import Meta

from app.core.response import SingleEntityResponse
from app.schemas.partner_competence import PartnerCompetenceCreate

from app.exceptions import UnprocessableEntity

from app.exceptions import UnfoundEntity

from app.schemas.partner_competence import PartnerCompetenceUpdate

router = APIRouter()


# Вывод всех партнерских компетенций
@router.get('/partner-competences/',
            response_model=ListOfEntityResponse,
            name='Список компетенций',
            description='Получение списка всех компетенций',
            tags=['Мобильное приложение / Партнерские компетенции']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_partner_competence.get_multi(db=session, page=None))

    data, paginator = crud_partner_competence.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_partner_competence(datum) for datum in data], meta=Meta(paginator=paginator))


# CREATE
@router.post('/partner-competences/',
             response_model=SingleEntityResponse,
             name='Создать партнерскую компетенцию',
             description='Создать партнерскую компетенцию, ',
             tags=['Админ панель / Партнерские компетенции']
             )
def create_partner_competence(
        new_data: PartnerCompetenceCreate,
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    obj = crud_partner_competence.get_by_name(db=session, name=new_data.name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такая компетенция уже есть",
            num=1,
            description="Компетенция с таким названием уже есть!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_partner_competence(crud_partner_competence.create(db=session, obj_in=new_data)))


# UPDATE
@router.put('/partner-competences/{partner_competences_id}/',
            response_model=SingleEntityResponse,
            name='Изменить название партнерской компетенции',
            description='Изменяет название партнерской компетенции',
            tags=['Админ панель / Партнерские компетенции'])
def update_implementation_stages(
        name: PartnerCompetenceUpdate,
        partner_competences_id: int = Path(..., title='Id партнерской компетенции'),
        session=Depends(deps.get_db)
):
    partner_competences, code, indexes = crud_partner_competence.update_partner_competences(
        db=session, new_data=name, id=partner_competences_id)
    if code == -1:
        raise UnfoundEntity(
            message="Партнерской компетенции с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Партнерской компетенции с таким названием уже есть!",
            num=2,
            description="Выберите другое название партнерской компетенции!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_partner_competence(db_obj=partner_competences))


# DELETE
@router.delete('/partner-competences/{partner_competences_id}/',
               response_model=SingleEntityResponse,
               name='Удалить партнерскую компетенцию',
               description='Полностью удаляет партнерскую компетенцию',
               tags=['Админ панель / Партнерские компетенции'])
def delete_partner_competences(
        partner_competences_id: int = Path(..., title='Id партнерской компетенции'),
        session=Depends(deps.get_db)
):
    if crud_partner_competence.get(db=session, id=partner_competences_id) is None:
        raise UnfoundEntity(
            message="Стадии реализации с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    return SingleEntityResponse(data=crud_partner_competence.remove(db=session, id=partner_competences_id))


if __name__ == "__main":
    logging.info('Running...')
