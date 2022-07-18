import logging

from fastapi import APIRouter, Depends

from app.api import deps
from app.core.response import SingleEntityResponse
from app.crud.crud_moderator import crud_moderator
from app.getters.moderator import get_moderator
from app.schemas.moderator import ModeratorCreate, ModeratorBase

from app.exceptions import UnprocessableEntity

router = APIRouter()


@router.post('/moderator/',
             response_model=SingleEntityResponse[ModeratorBase],
             name='Создать модератора',
             description='Создать модератора, ',
             tags=['Админка']
             )
def create_moderator(
        new_data: ModeratorCreate,
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    db_obj = crud_moderator.get_by_login(db=session, login=new_data.login)
    if db_obj is not None:
        raise UnprocessableEntity(
            message="Модератор с таким логином уже существует!",
            num=2,
            description="Попробуйте изменить логин для нового модератора!",
            path="$.body"
        )
    # ПРОВЕРИТЬ ЯВЛЯЕТСЯ ЛИ current_user СУПЕР-ЮЗЕРОМ
    return SingleEntityResponse(data=get_moderator(crud_moderator.create(db=session, obj_in=new_data)))


if __name__ == "__main":
    logging.info('Running...')
