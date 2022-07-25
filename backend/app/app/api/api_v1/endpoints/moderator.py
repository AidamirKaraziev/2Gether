import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
# from fastapi.params import Path, Form

from app.api import deps
from app.core.response import SingleEntityResponse, ListOfEntityResponse, Meta
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

from app.utils.time_stamp import date_from_timestamp

from app.getters.moderator import get_moderator_delete

router = APIRouter()


# Вход по логину и паролю
@router.post('/cp/sign-in/', response_model=SingleEntityResponse[TokenBase],
             name='Войти в админ панель',
             description='Войти в админ панель',
             tags=['Вход / Админ панель'])
def entrance(
    moderator: ModeratorEntrance,
    session=Depends(deps.get_db),
):
    db_obj = crud_moderator.get_moderator(session, moderator=moderator)
    token = create_token_moderator(subject=db_obj.id)
    return SingleEntityResponse(data=TokenBase(token=token))


# CREATE
@router.post('/cp/moderators/',
             response_model=SingleEntityResponse[ModeratorGet],
             name='Создать модератора',
             description='Создать модератора, ',
             tags=['Админ панель / Модератор']
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
            num=1,
            description="Попробуйте изменить логин для нового модератора!",
            path="$.body"
        )
    if admin.is_superuser is not True:
        raise InaccessibleEntity(
            message="Модератор не обладает правами!",
            num=2,
            description="Модератор не обладает правами, к созданию других модераторов!",
            path="$.body"
        )
    # проверка локации и зоны ответственности
    if new_data.location_id is not None:
        loc = crud_location.get(db=session, id=new_data.location_id)
        if loc is None:
            raise UnfoundEntity(
                message="Такого города нет!",
                num=3,
                description="Введен неправильный id города!",
                path="$.body"
            )
    if new_data.area_of_responsibility_id is not None:
        if crud_area_of_responsibility.get(db=session, id=new_data.area_of_responsibility_id) is None:
            raise UnfoundEntity(
                message="Нет такой зоны ответственности!",
                num=4,
                description="Введен неправильный id зоны ответственности!",
                path="$.body"
            )
    db_obj = crud_moderator.get_by_login(db=session, login=new_data.login)
    if db_obj is not None:
        raise UnprocessableEntity(
            message="Модератор с таким логином уже существует!",
            num=5,
            description="Попробуйте изменить логин для нового модератора!",
            path="$.body"
        )
    psw = get_password_hash(password=new_data.password)
    new_data.password = psw
    if new_data.birthday is not None:
        new_data.birthday = date_from_timestamp(new_data.birthday)
    return SingleEntityResponse(data=get_moderator(crud_moderator.create(db=session, obj_in=new_data), request=request))


# Апи удаления модератора АДМИНОМ
@router.delete("/cp/moderators/{moderator_id}/",
               response_model=SingleEntityResponse,
               name='Удаление модератора',
               description='Модератора удаляет админ',
               tags=['Админ панель / Модератор'])
def remove_with_path(
        request: Request,
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
    # return SingleEntityResponse(data=crud_moderator.remove(db=session, id=db_obj.id))
    # return SingleEntityResponse(data=get_moderator(
    #     crud_moderator.remove(db=session, id=moderator_id), request=request))
    return SingleEntityResponse(data=get_moderator_delete(crud_moderator.remove(db=session, id=moderator_id), request=request))


# GET
@router.get('/cp/moderators/me/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Получить данные профиля модератора',
            description='Получение всех  данных профиля модератора, по токену',
            tags=['Админ панель / Профиль']
            )
def get_data(
        request: Request,
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
):
    return SingleEntityResponse(data=get_moderator(current_moderator, request=request))  # request=request


# DELETE
@router.delete("/cp/moderators/me/",
               response_model=SingleEntityResponse,
               name='Удаляет текущего модератора',
               description='Модератор сам удаляет свой акк',
               tags=['Админ панель / Профиль'])
def remove_with_path(
        request: Request,
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db)
):
    return SingleEntityResponse(data=get_moderator_delete(
        crud_moderator.remove(db=session, id=current_moderator.id), request=request))


# UPDATE PHOTO BY TOKEN
@router.put("/cp/moderators/me/photos/",
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить фотографию',
            description='Изменить фотографию в профиле, если отправить пустой файл сбрасывает фото в профиле',
            tags=['Админ панель / Профиль'],
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


# UPDATE PHOTO FOR ADMIN
@router.put("/cp/moderators/{moderator_id}/photos/",
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить фотографию модератора',
            description='Изменить фотографию модератора, Админом. Если отправить пустой файл сбрасывает фото в профиле',
            tags=['Админ панель / Модератор'],
            )
def create_upload_file(
        request: Request,
        moderator_id: int = Path(..., title='Id проекта'),
        file: Optional[UploadFile] = File(None),
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
        ):
    # Надо будет проверить является ли он супер пупер админом
    db_obj, code, index = crud_moderator.check_is_superuser(db=session, current_moderator=current_moderator)
    if code == -1:
        raise UnfoundEntity(
            message="Администратора не существует",
            num=1,
            description="Нет id модератора в базе данных",
            path="$.body"
        )
    if code == -2:
        raise InaccessibleEntity(
            message="Нет доступа к изменению!",
            num=2,
            description="Менять модераторов могут только администраторы",
            path="$.body"
        )
    if db_obj:
        if crud_moderator.get(db=session, id=moderator_id) is None:
            raise UnfoundEntity(
                message="Модератора не существует",
                num=3,
                description="Нет id модератора в базе данных",
                path="$.body"
            )
        save_path = crud_moderator.adding_photo(db=session, file=file, id_moderator=moderator_id)
        if not save_path:
            raise UnfoundEntity(message="Не отправлен загружаемый файл",
                                num=4,
                                description="Попробуйте загрузить файл еще раз",
                                path="$.body",
                                )
    mod = crud_moderator.get(db=session, id=moderator_id)
    return SingleEntityResponse(data=get_moderator(mod, request=request))


# GET ALL MODERATOR
@router.get('/cp/moderators/',
            response_model=ListOfEntityResponse,
            name='Список всех модераторов',
            description='Получение списка всех модераторов',
            tags=['Админ панель / Модератор']
            )
def get_data(
        request: Request,
        session=Depends(deps.get_db),
        page: int = Query(1, title="Номер страницы")
):
    logging.info(crud_moderator.get_multi(db=session, page=None))
    data, paginator = crud_moderator.get_multi(db=session, page=page)
    return ListOfEntityResponse(data=[get_moderator(request=request, moderator=datum) for datum in data],
                                meta=Meta(paginator=paginator))


# GET MODERATOR BY ID
@router.get('/cp/moderators/{moderator_id}/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Получить данные модератора',
            description='Получение всех данных модератора, по id',
            tags=['Админ панель / Модератор']
            )
def get_data(
        request: Request,
        moderator_id: int = Path(..., title='Id проекта'),
        session=Depends(deps.get_db),
):
    moderator = crud_moderator.get(db=session, id=moderator_id)
    if moderator is None:
        raise UnprocessableEntity(
            message="Такого модератора не обнаружено!",
            num=1,
            description="Попробуйте еще раз!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_moderator(moderator=moderator, request=request))


# UPDATE MODERATOR FOR ADMIN
@router.put('/cp/moderators/{moderator_id}/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить данные модератора',
            description='Изменить данные этого модератора',
            tags=['Админ панель / Модератор']
            )
def update_moderator(
        request: Request,
        new_data: ModeratorRequest,
        moderator_id: int = Path(..., title='Id модератора'),
        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
):
    moderator, code, indexes = crud_moderator.update_moderator(db=session, obj_in=new_data,
                                                               moderator_id=moderator_id,
                                                               current_moderator=current_moderator)
    if code == -1:
        raise InaccessibleEntity(
            message="Нет доступа к изменению!",
            num=1,
            description="Менять модераторов могут только администраторы",
            path="$.body"
        )
    if code == -2:
        raise UnfoundEntity(
            message="Модератора не существует",
            num=2,
            description="Нет id модератора в базе данных",
            path="$.body"
        )
    if code == -3:
        raise UnfoundEntity(
            message="Нет такого города!",
            num=3,
            description="Попробуйте выбрать город еще раз!",
            path="$.body"
        )
    if code == -4:
        raise UnfoundEntity(
            message="Нет такой зоны ответственности ",
            num=4,
            description="Введите существующую зону ответственности",
            path="$.body",
        )

    return SingleEntityResponse(data=get_moderator(moderator=moderator, request=request))


# UPDATE
@router.put('/cp/moderators/me/',
            response_model=SingleEntityResponse[ModeratorGet],
            name='Изменить данные модератора',
            description='Изменить данные текущего модератора',
            tags=['Админ панель / Профиль']
            )
def update_moderator(
        request: Request,
        new_data: ModeratorRequest,

        current_moderator=Depends(deps.get_current_moderator_by_bearer),
        session=Depends(deps.get_db),
):

    db_obj, code, index = crud_moderator.update_moderator_self(
        db=session, current_moderator=current_moderator, obj_in=new_data)
    if code == -1:
        raise UnfoundEntity(
            message="Модератора с таким id не существует!",
            num=1,
            description="Модератора с таким id не существует!",
            path="$.body"
        )
    if code == -2:
        raise UnfoundEntity(message="Неправильно указан город",
                            num=4,
                            description="Попробуйте указать город еще раз!",
                            path="$.body",
                            )
    if code == -3:
        raise UnfoundEntity(message="Нет такой зоны ответственности",
                            num=5,
                            description="Попробуйте указать зону ответственности еще раз!",
                            path="$.body",
                            )
    if code == -4:
        raise InaccessibleEntity(message="Вы не обладаете правами назначать себя администратором",
                                 num=3,
                                 description="Вы не обладаете правами!",
                                 path="$.body",
                                 )
    if code == -5:
        raise InaccessibleEntity(message="Вы не обладаете правами назначать себе зоны ответственности",
                                 num=2,
                                 description="Вы не обладаете правами!",
                                 path="$.body",
                                 )

    # crud_moderator.update(db=session, db_obj=current_moderator, obj_in=new_data)
    return SingleEntityResponse(data=get_moderator(db_obj, request=request))


if __name__ == "__main":
    logging.info('Running...')
