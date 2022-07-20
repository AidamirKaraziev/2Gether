import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File
# from fastapi.params import Path, Form

from app.api import deps
from app.core.response import SingleEntityResponse
from app.crud.crud_moderator import crud_moderator
from app.getters.moderator import get_moderator
from app.schemas.moderator import ModeratorCreate, ModeratorBase, ModeratorRequest, ModeratorEntrance

from app.exceptions import UnprocessableEntity, UnfoundEntity, InaccessibleEntity

from app.core.security import create_token

from app.schemas.token import TokenBase

from app.example.security import create_token_moderator

from app.getters.moderator import get_moderator_for_create

from app.core.security import get_password_hash

from app.schemas.moderator import ModeratorGet
from fastapi.params import Path

from app.crud.area_of_responsibility import crud_area_of_responsibility
from app.crud.crud_location import crud_location


router = APIRouter()


@router.post('/cp/moderators/',
             response_model=SingleEntityResponse[ModeratorGet],
             name='Создать модератора',
             description='Создать модератора, ',
             tags=['Админ']
             )
def create_moderator(
        request: Request,
        new_data: ModeratorRequest,
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
):

    admin = crud_moderator.get(db=session, id=current_moderator.id)
    if admin is None:
        raise UnfoundEntity(
            message="Админа с таким id не существует!",
            num=2,
            description="Попробуйте изменить логин для нового модератора!",
            path="$.body"
        )
    if admin.is_superuser is not True:
        raise InaccessibleEntity(
            message="Модератор не обладает правами!",
            num=3,
            description="Модератор не обладает правами, к созданию других модераторов!",
            path="$.body"
        )
    db_obj = crud_moderator.get_by_login(db=session, login=new_data.login)
    if db_obj is not None:
        raise UnprocessableEntity(
            message="Модератор с таким логином уже существует!",
            num=4,
            description="Попробуйте изменить логин для нового модератора!",
            path="$.body"
        )
    psw = get_password_hash(password=new_data.password)
    new_data.password = psw
    return SingleEntityResponse(data=get_moderator(crud_moderator.create(db=session, obj_in=new_data), request=request))


# Вход по логину и паролю
@router.post('/cp/sign-in/', response_model=SingleEntityResponse[TokenBase],
             name='Войти в админ панель',
             description='Войти в админ панель',
             tags=['Админка'])
def entrance(
    moderator: ModeratorEntrance,
    session=Depends(deps.get_db),
):
    db_obj = crud_moderator.get_moderator(session, moderator=moderator)
    token = create_token_moderator(subject=db_obj.id)
    return SingleEntityResponse(data=TokenBase(token=token))


# GET
@router.get('/cp/profile/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Получить данные профиля модератора',
            description='Получение всех  данных профиля модератора, по токену',
            tags=['Модератор']
            )
def get_data(
        request: Request,
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
):
    return SingleEntityResponse(data=get_moderator(current_moderator, request=request))  # request=request


# Апи удаления модератора
@router.delete("/cp/moderators/profile/",
               response_model=SingleEntityResponse,
               name='Удаляет текущего модератора',
               description='Модератор сам удаляет свой акк',
               tags=['Модератор'])
def remove_with_path(
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db)
):
    return SingleEntityResponse(data=crud_moderator.remove(db=session, id=current_moderator.id))


# Апи удаления модератора АДМИНОМ
@router.delete("/cp/moderators/{moderator_id}/",
               response_model=SingleEntityResponse,
               name='Удаление модератора',
               description='Модератора удаляет админ',
               tags=['Админ'])
def remove_with_path(
        moderator_id: int = Path(...),
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj = crud_moderator.get(db=session, id=moderator_id)
    if db_obj is None:
        raise UnfoundEntity(
            message="Нет модератора с таким идентификатором!",
            num=1,
            description="Такого модератора не существует!",
            path="$.body"
        )
    if not current_moderator.is_superuser:
        raise InaccessibleEntity(
            message="Модератор не обладает правами!",
            num=2,
            description="Модератор не обладает правами, к удалению других модераторов!",
            path="$.body"
        )
    return SingleEntityResponse(data=crud_moderator.remove(db=session, id=db_obj.id))


# Изменить данные модератора
@router.put('/cp/moderators/profile/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить данные модератора',
            description='Изменить данные текущего модератора',
            tags=['Модератор']
            )
def update_moderator(
        request: Request,
        new_data: ModeratorRequest,

        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
):
    # проверять администратор ли это пока что не надо
    # if current_moderator.is_superuser:
    #     raise UnprocessableEntity(
    #         message="Это апи предназначается модераторам!",
    #         num=1,
    #         description="Это апи предназначается модераторам, а не администраторам",
    #         path="$.body"
    #     )
    moderator = crud_moderator.get(db=session, id=current_moderator.id)
    if moderator is None:
        raise UnprocessableEntity(
            message="Модератора с таким id не существует!",
            num=2,
            description="Модератора с таким id не существует!",
            path="$.body"
        )

    # ВОТ ЗДЕСЬ ПРОВЕРЯТЬ ЕСТЬ ЛИ ТАКАЯ ID ЛОКАЦИИ
    if new_data.location_id in new_data:
        loc = crud_location.get(db=session, id=new_data.location_id)
        if loc is None:
            raise UnfoundEntity(message="Неправильно указан город",
                                num=3,
                                description="Попробуйте указать город еще раз!",
                                path="$.body",
                                )
    if new_data.area_of_responsibility_id in new_data:
        aor = crud_area_of_responsibility.get(db=session, id=new_data.area_of_responsibility_id)
        if aor is None:
            raise UnfoundEntity(message="Нет такой сферы деятельности",
                                num=4,
                                description="Попробуйте указать сферу деятельности еще раз!",
                                path="$.body",
                                )

    crud_moderator.update(db=session, db_obj=current_moderator, obj_in=new_data)
    return SingleEntityResponse(data=get_moderator(current_moderator, request=request))


@router.put("/cp/moderators/profile/photo/",
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить фотографию',
            description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
            tags=['Модератор'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
        ):
    moderator_id = current_moderator.id
    save_path = crud_moderator.adding_photo(db=session, file=file, id_moderator=moderator_id)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=get_moderator(current_moderator, request=request))


if __name__ == "__main":
    logging.info('Running...')
