import logging

from fastapi import APIRouter, Depends, Query

from app.core.response import ListOfEntityResponse
from app.crud.crud_partner_competence import crud_partner_competence
from app.getters.partner_competence import get_partner_competence

from app.api import deps

from app.core.response import Meta

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


if __name__ == "__main":
    logging.info('Running...')
