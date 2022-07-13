import logging

from fastapi import APIRouter, Depends, Query

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.activity_sphere import crud_activity_sphere
from app.getters.activity_sphere import get_activity_sphere

router = APIRouter()


# Вывод всех локаций
@router.get('/activity-sphere/',
            response_model=ListOfEntityResponse,
            name='Список сфер деятельности',
            description='Получение списка всех сфер деятельности',
            tags=['Инструменты']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_activity_sphere.get_multi(db=session, page=None))

    data, paginator = crud_activity_sphere.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_activity_sphere(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main":
    logging.info('Running...')
