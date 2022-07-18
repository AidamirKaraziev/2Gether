import logging

from fastapi import APIRouter, Depends, Query

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.area_of_responsibility import crud_area_of_responsibility
from app.getters.area_of_responsibility import get_area_of_responsibility

router = APIRouter()


# Вывод всех локаций
@router.get('/area-of-responsibility/',
            response_model=ListOfEntityResponse,
            name='Список зон ответственности',
            description='Получение списка всех зон ответственности',
            tags=['Инструменты']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_area_of_responsibility.get_multi(db=session, page=None))

    data, paginator = crud_area_of_responsibility.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_area_of_responsibility(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main":
    logging.info('Running...')
