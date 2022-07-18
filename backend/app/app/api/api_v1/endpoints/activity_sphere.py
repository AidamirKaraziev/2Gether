import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, Request, UploadFile, File, Form

from app.api import deps
from app.core.response import ListOfEntityResponse, Meta
from app.crud.crud_activity_sphere import crud_activity_sphere
from app.getters.activity_sphere import get_activity_sphere

from app.core.response import SingleEntityResponse
from app.schemas.activity_sphere import ActivitySphereCreate

from app.exceptions import UnprocessableEntity

from app.exceptions import UnfoundEntity

from app.getters.activity_sphere import get_picture

from app.schemas.activity_sphere import ActivitySpherePictureCreate

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


# Написать апи по добавлению новых сфер деятельности с сохранением эмблемки
@router.post('/activity-sphere/',
             response_model=SingleEntityResponse,
             name='Добавить сферу деятельности',
             description='Добавить сферу деятельности',
             tags=['Админка']
             )
def create_activity_sphere(
        new_data: ActivitySphereCreate,
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    obj = crud_activity_sphere.get_by_name(db=session, name=new_data.name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такая сфера деятельности уже имеется",
            num=1,
            description="Сфера деятельности с таким названием уже имеется!",
            path="$.body"
        )
    return SingleEntityResponse(
        data=get_activity_sphere(crud_activity_sphere.create(db=session, obj_in=new_data)))


# Эксперимент: Сделать создание и добавление картинки в одном апи
@router.post("/activity-sphere/picture/",
             response_model=SingleEntityResponse,
             name='Добавить сферу деятельности',
             description='Добавить сферу деятельности',
             tags=['Админка']
             )
def create_upload_file(

        name: str = Form(...),

        request: Request = Form(...),
        file: Optional[UploadFile] = File(None),

        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):

    obj = crud_activity_sphere.get_by_name(db=session, name=name)
    if obj is not None:
        raise UnprocessableEntity(
            message="Такая сфера деятельности уже имеется",
            num=1,
            description="Сфера деятельности с таким названием уже имеется!",
            path="$.body"
        )
    save_path = crud_activity_sphere.adding_photo(file=file)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    response = get_picture(path_name=save_path, request=request, )
    s = ActivitySpherePictureCreate(name=name, picture=response.picture)
    return SingleEntityResponse(
        data=get_activity_sphere(crud_activity_sphere.create(db=session, obj_in=s)))


if __name__ == "__main":
    logging.info('Running...')
