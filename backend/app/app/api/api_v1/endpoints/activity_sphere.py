import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, Request, UploadFile, File, Form, Path

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

from app.schemas.activity_sphere import ActivitySphereUpdate

from app.schemas.activity_sphere import ActivitySpherePicture

router = APIRouter()


# Вывод всех сфер деятельности
@router.get('/activity-spheres/',
            response_model=ListOfEntityResponse,
            name='Список сфер деятельности',
            description='Получение списка всех сфер деятельности',
            tags=['Мобильное приложение / Сферы деятельности']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_activity_sphere.get_multi(db=session, page=None))
    data, paginator = crud_activity_sphere.get_multi(db=session, page=page)
    return ListOfEntityResponse(data=[get_activity_sphere(request=request, db_obj=datum) for datum in data], meta=Meta(paginator=paginator))


@router.post("/activity-spheres/",
             response_model=SingleEntityResponse,
             name='Добавить сферу деятельности',
             description='Добавить сферу деятельности',
             tags=['Админ панель / Сферы деятельности']
             )
def create_upload_file(
        request: Request,
        name: str = Form(...),
        # request: Request = Form(...),
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
    # создаем ссылку до папки
    save_path = crud_activity_sphere.adding_photo(file=file)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    # формирует url ссылку
    response = get_picture(path_name=save_path, request=request, )

    s = ActivitySpherePictureCreate(name=name, picture=save_path)
    return SingleEntityResponse(
        data=get_activity_sphere(db_obj=crud_activity_sphere.create(db=session, obj_in=s), request=request))
# Эксперимент: Сделать создание и добавление картинки в одном апи


# UPDATE
@router.put('/activity-spheres/{activity_spheres_id}/',
            response_model=SingleEntityResponse,
            name='Изменить название сферы деятельности',
            description='Изменяет название сферы деятельности',
            tags=['Админ панель / Сферы деятельности'])
def update_activity_spheres_name(
        request: Request,
        name: ActivitySphereUpdate,
        activity_spheres_id: int = Path(..., title='Id партнерской компетенции'),
        session=Depends(deps.get_db)
):
    activity_spheres, code, indexes = crud_activity_sphere.update_activity_spheres(
        db=session, new_data=name, id=activity_spheres_id)
    if code == -1:
        raise UnfoundEntity(
            message="Сферы деятельности с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Сферы деятельности с таким названием уже есть!",
            num=2,
            description="Выберите другое название сферы деятельности!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_activity_sphere(db_obj=activity_spheres, request=request))


# UPDATE PHOTOS
@router.put('/activity-spheres/picture/{activity_spheres_id}/',
            response_model=SingleEntityResponse,
            name='Изменить картинку сферы деятельности',
            description='Изменяет название сферы деятельности',
            tags=['Админ панель / Сферы деятельности'])
def update_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        # name: ActivitySphereUpdate,
        activity_spheres_id: int = Path(..., title='Id партнерской компетенции'),
        session=Depends(deps.get_db)
):
    obj = crud_activity_sphere.get(db=session, id=activity_spheres_id)
    if obj is None:
        raise UnprocessableEntity(
            message="Такой сфера деятельности нет!",
            num=1,
            description="Сферы деятельности с таким названием нет!",
            path="$.body"
        )
    save_path = crud_activity_sphere.adding_photo(file=file)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    obj_in = ActivitySpherePicture(picture=save_path)

    return SingleEntityResponse(
        data=get_activity_sphere(db_obj=(crud_activity_sphere.update(db=session, db_obj=obj, obj_in=obj_in)), request=request))


# DELETE
@router.delete('/activity-spheres/{activity_spheres_id}/',
               response_model=SingleEntityResponse,
               name='Удалить сферу деятельности',
               description='Полностью удаляет сферу деятельности',
               tags=['Админ панель / Сферы деятельности'])
def delete_partner_competences(
        request: Request,
        activity_spheres_id: int = Path(..., title='Id сферы деятельности'),
        session=Depends(deps.get_db)
):
    if crud_activity_sphere.get(db=session, id=activity_spheres_id) is None:
        raise UnfoundEntity(
            message="Сферы деятельности с таким id нет!",
            num=1,
            description="Введите корректный id!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_activity_sphere(
        db_obj=(crud_activity_sphere.remove(db=session, id=activity_spheres_id)), request=request))


if __name__ == "__main":
    logging.info('Running...')
