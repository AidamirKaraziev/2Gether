import logging

from fastapi import APIRouter, Depends, Query

from app.core.response import ListOfEntityResponse
from app.crud.crud_partner_competence import crud_partner_competence
from app.getters.partner_competence import get_partner_competence

from app.api import deps

from app.core.response import Meta

from app.core.response import SingleEntityResponse
from app.schemas.partner_competence import PartnerCompetenceCreate

from app.exceptions import UnprocessableEntity

router = APIRouter()


# Вывод всех локаций
@router.get('/partner-competence/',
            response_model=ListOfEntityResponse,
            name='Список компетенций',
            description='Получение списка всех компетенций',
            tags=['Инструменты']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_partner_competence.get_multi(db=session, page=None))

    data, paginator = crud_partner_competence.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_partner_competence(datum) for datum in data], meta=Meta(paginator=paginator))


@router.post('/partner-competence/',
             response_model=SingleEntityResponse,
             name='Создать партнерскую компетенцию',
             description='Создать партнерскую компетенцию, ',
             tags=['Админка']
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


if __name__ == "__main":
    logging.info('Running...')
