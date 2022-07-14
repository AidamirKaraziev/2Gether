from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request

from app.crud import verif_codes_service as service
from app.crud.crud_user import crud_user

from app.schemas.verif_code import CheckCode, GettingVerifCode, UsedVerifCode
from app.schemas.user import UserCreate, UserBase
from app.schemas.token import TokenBase

from app.core.security import create_token
from app.core.response import SingleEntityResponse, OkResponse

from app.exceptions import UnprocessableEntity

from app.api import deps


router = APIRouter()


@router.post('/sign-in/', response_model=SingleEntityResponse[TokenBase],
             name='Войти в приложение',
             description='Войти в приложение, используя телефон и код подтверждения',
             tags=['Вход'])
def check_code(
    request: Request,
    check_code_data: CheckCode,
    session=Depends(deps.get_db),
    x_real_ip: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_firebase_token: Optional[str] = Header(None)
):

    data, code, indexes = service.check_code_test(db=session, tel=check_code_data.tel, code=check_code_data.value)

    # обработка исключений того что вернул
    if code == -1:
        raise UnprocessableEntity(
            message="Номер не найден",
            num=2,
            description="Попробуйте ввести номер еще раз",
            path="$.body",
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Неправильно введенный код!",
            num=2,
            description="Попробуйте ввести код еще раз!",
            path="$.body"
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Код уже использовался! Запросите новый!",
            num=2,
            description="Попробуйте запросить новый код!",
            path="$.body"
        )

    if code == -4:
        raise UnprocessableEntity(
            message="Время истекло, запросите новый код!",
            num=2,
            description="Попробуйте запросить новый код!",
            path="$.body"
            )

    # проверяем есть ли юзер с таким номером
    user = crud_user.get_by_tel(db=session, tel=check_code_data.tel)
    if user is None:
        case_for_save = UserCreate(tel=check_code_data.tel)
        user = crud_user.create(db=session, obj_in=case_for_save)

    crud_user._handle_device(db=session,
                             owner=user,
                             host=request.client.host,
                             x_real_ip=x_real_ip,
                             accept_language=accept_language,
                             user_agent=user_agent,
                             x_firebase_token=x_firebase_token)

    used = UsedVerifCode(actual=False)
    service.update(db=session, db_obj=data, obj_in=used)

    # Заменить снизу на генерацию и отправку токена
    token = create_token(subject=user.id)
    return SingleEntityResponse(data=TokenBase(token=token))
