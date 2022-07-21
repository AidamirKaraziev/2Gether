import logging

from fastapi import APIRouter, Depends, Query, Path

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.crud_stage_of_implementation import crud_stage_of_implementation
from app.getters.stage_of_implementation import get_stage_of_implementation

from app.core.response import SingleEntityResponse
from app.exceptions import UnprocessableEntity, UnfoundEntity
from app.schemas.stage_of_implementation import StageOfImplementationCreate

from app.schemas.stage_of_implementation import StageOfImplementationUpdate

router = APIRouter()


@router.get('/implementation-stages/',
            response_model=ListOfEntityResponse,
            name='Список со стадиями проектов',
            description='Получение списка всех возможных стадий проекта',
            tags=['Мобильное приложение / Стадии реализации']
            )
def get_data(
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_stage_of_implementation.get_multi(db=session, page=None))

    data, paginator = crud_stage_of_implementation.get_multi(db=session, page=page)

    return ListOfEntityResponse(data=[get_stage_of_implementation(datum) for datum in data],
                                meta=Meta(paginator=paginator))


# Создание стадии реализации
@router.post('/implementation-stages/',
             response_model=SingleEntityResponse,
             name='Добавить стадию реализации',
             description='Добавить одну стадию реализации в базу данных ',
             tags=['Админ панель / Стадии реализации']
             )
def create_partner_competence(
        new_data: StageOfImplementationCreate,
        session=Depends(deps.get_db),
):
    obj = crud_stage_of_implementation.get_by_name(db=session, name=new_data.name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такая стадия реализации уже есть в базе данных",
            num=1,
            description="Стадия реализации с таким названием уже есть в базе данных!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_stage_of_implementation(
        crud_stage_of_implementation.create(db=session, obj_in=new_data)))


# Апи удаляет стадию реализации
@router.delete('/implementation-stages/{implementation_stages_id}/',
               response_model=SingleEntityResponse,
               name='Удалить стадию реализации',
               description='Полностью удаляет стадию реализации',
               tags=['Админ панель / Стадии реализации'])
def delete_implementation_stages(
        implementation_stages_id: int = Path(..., title='Id проекта'),
        session=Depends(deps.get_db)
):
    if crud_stage_of_implementation.get(db=session, id=implementation_stages_id) is None:
        raise UnfoundEntity(
            message="Стадии реализации с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    return SingleEntityResponse(data=crud_stage_of_implementation.remove(db=session, id=implementation_stages_id))


# ИЗМЕНИТЬ
@router.put('/implementation-stages/{implementation_stages_id}/',
            response_model=SingleEntityResponse,
            name='Изменить название стадии реализации',
            description='Изменяет название стадии реализации',
            tags=['Админ панель / Стадии реализации'])
def update_implementation_stages(
        name: StageOfImplementationUpdate,
        implementation_stages_id: int = Path(..., title='Id стадии реализации'),
        session=Depends(deps.get_db)
):
    implementation_stages, code, indexes = crud_stage_of_implementation.update_location(
        db=session, new_data=name, id=implementation_stages_id)
    if code == -1:
        raise UnfoundEntity(
            message="Стадии реализации с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Стадия реализации с таким названием уже есть!",
            num=2,
            description="Выберите другое название стадии реализации!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_stage_of_implementation(db_obj=implementation_stages))


if __name__ == "__main":
    logging.info('Running...')
