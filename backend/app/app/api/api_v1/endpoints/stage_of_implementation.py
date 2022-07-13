import logging

from fastapi import APIRouter, Depends, Query

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.crud_stage_of_implementation import crud_stage_of_implementation
from app.getters.stage_of_implementation import get_stage_of_implementation

router = APIRouter()


@router.get('/stage-of-implementation/',
            response_model=ListOfEntityResponse,
            name='Список со стадиями проектов',
            description='Получение списка всех возможных стадий проекта',
            tags=['Инструменты']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_stage_of_implementation.get_multi(db=session, page=None))

    data, paginator = crud_stage_of_implementation.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_stage_of_implementation(datum) for datum in data],
                                meta=Meta(paginator=paginator))


if __name__ == "__main":
    logging.info('Running...')
