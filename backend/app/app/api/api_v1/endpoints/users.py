import logging
from os.path import isfile
from typing import Optional
from mimetypes import guess_type

from fastapi import APIRouter, Header, Depends, UploadFile, File, HTTPException
from fastapi import Response, Request
from fastapi.params import Path

from app.api import deps
from app.core.response import SingleEntityResponse, OkResponse, ListOfEntityResponse

from app.crud.crud_user import crud_user
from app.crud.crud_project import crud_project
from app.crud.crud_location import crud_location
from app.crud import verif_codes_service as service

from app.schemas.user import UserBase, UserBasicUpdate
from app.schemas.verif_code import CheckCode, UsedVerifCode
from app.schemas import UserUpdateTel, UserGet

from app.getters.user import get_user
from app.exceptions import UnfoundEntity, UnprocessableEntity

from app.utils.time_stamp import date_from_timestamp


router = APIRouter()


@router.get("/static/{filename:path}", name='Получить статический файл', tags=['Инструменты'])
async def get_site(filename):
    filename = 'static/' + filename
    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, 'rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


# GET
@router.get('/users/me/',
            response_model=SingleEntityResponse[UserGet],
            name='Получить данные профиля',
            description='Получение всех  данных профиля, по токену',
            tags=['Мобильное приложение / Профиль']
            )
def get_data(
        request: Request,
        current_user=Depends(deps.get_current_user_by_bearer),
):
    return SingleEntityResponse(data=get_user(current_user, request=request))  # request=request


# Изменить данные пользователя
@router.put('/users/me/',
            response_model=SingleEntityResponse[UserGet],
            name='Изменить данные профиля',
            description='Изменить данные текущего пользователя',
            tags=['Мобильное приложение / Профиль']
            )
def update_user(
        request: Request,
        new_data: UserBasicUpdate,

        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    # ВОТ ЗДЕСЬ ПРОВЕРЯТЬ ЕСТЬ ЛИ ТАКОЙ ID ЛОКАЦИИ
    if new_data.location_id in new_data:
        loc = crud_location.get(db=session, id=new_data.location_id)
        if loc is None:
            raise UnfoundEntity(message="Неправильно указан город",
                                num=0,
                                description="Попробуйте указать город еще раз!",
                                path="$.body",
                                )
    if new_data.birthday is not None:
        new_data.birthday = date_from_timestamp(new_data.birthday)
    crud_user.update(db=session, db_obj=current_user, obj_in=new_data)
    return SingleEntityResponse(data=get_user(current_user, request=request))


@router.put("/users/me/photos/{num}/",
            response_model=SingleEntityResponse[UserGet],
            name='Изменить фотографию профиля',
            description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
            tags=['Мобильное приложение / Профиль'],
            )
def create_upload_file(
        request: Request,
        num: str = Path(...),
        file: Optional[UploadFile] = File(None),
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    if num not in ["main", "1", "2"]:
        raise UnfoundEntity(
            message="Неправильный num",
            num=2,
            description="Введите правильный num",
            path="$.body",
        )
    user_id = current_user.id
    save_path = crud_user.adding_photo(db=session, num=num, file=file, id_user=user_id)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_user(current_user, request=request))


# Апи удаления юзера
@router.delete("/users/me/",
               response_model=SingleEntityResponse[UserGet],
               name='Удаляет текущего пользователя',
               description='Полностью удаляет текущего пользователя',
               tags=['Мобильное приложение / Профиль'])
def remove_with_path(
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db)
):
    return SingleEntityResponse(data=crud_user.remove(db=session, id_user=current_user.id))


# Замена номера телефона в текущем аккаунте
@router.put('/users/me/tel/', response_model=SingleEntityResponse[UserGet],
            name='Изменить номер телефона профиля',
            description='Изменить номер телефона, используя телефон, код подтверждения и старый токен',
            tags=['Мобильное приложение / Профиль'])
def check_code(
        request: Request,
        check_code_data: CheckCode,
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),

):
    # проверяем есть ли пользователь с таким номером
    user = crud_user.get_by_tel(db=session, tel=check_code_data.tel)
    if user is not None:
        raise UnprocessableEntity(
            message="Пользователь с таким номером уже есть в базе!",
            num=1,
            description="Используйте номер который ранее не использовался!",
            path="$.body"
        )

    data, code, indexes = service.check_code_test(db=session,
                                                  tel=check_code_data.tel,
                                                  code=check_code_data.value)

    # обработка исключений того что вернул
    if code == -1:
        raise UnprocessableEntity(
            message="Номер указан неправильно",
            num=2,
            description="Попробуйте ввести номер еще раз",
            path="$.body",
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Неправильно введенный код!",
            num=3,
            description="Попробуйте ввести код еще раз!",
            path="$.body"
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Код уже использовался! Запросите новый!",
            num=4,
            description="Попробуйте запросить новый код!",
            path="$.body"
        )

    if code == -4:
        raise UnprocessableEntity(
            message="Время истекло, запросите новый код!",
            num=5,
            description="Попробуйте запросить новый код!",
            path="$.body"
            )

    used = UsedVerifCode(actual=False)
    service.update_actual(db=session, db_obj=data, obj_in=used)

    # Если юзера с таким номером нет в базе
    update_data = UserUpdateTel(tel=check_code_data.tel)
    db_obj = crud_user.update_tel(db=session, db_obj=current_user, obj_in=update_data)
    return SingleEntityResponse(data=get_user(db_obj, request=request))


# Вывод всех проектов пользователя
@router.get('/users/me/projects/',
            response_model=ListOfEntityResponse,
            name='Список проектов профиля',
            description='Получение списка всех проектов данного пользователя',
            tags=['Мобильное приложение / Профиль']
            )
def get_data(
        # user_id: int = Path(..., title='Id пользователя'),
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    data = crud_project.get_multi_project(db=session, user_id=current_user.id)
    return ListOfEntityResponse(data=data)


if __name__ == "__main":
    logging.info('Running...')
