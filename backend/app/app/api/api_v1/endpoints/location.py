import logging

from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException, Query

from app.core.response import ListOfEntityResponse
from app.crud.crud_location import crud_location

from app.api import deps

from app.core.response import Meta
from app.getters.location import get_location

router = APIRouter()


# Вывод всех локаций
@router.get('/locations/',
            response_model=ListOfEntityResponse,
            name='Список городов',
            description='Получение списка всех городов',
            tags=['Инструменты']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_location.get_multi(db=session, page=None))

    data, paginator = crud_location.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_location(datum) for datum in data], meta=Meta(paginator=paginator))


if __name__ == "__main":
    logging.info('Running...')
