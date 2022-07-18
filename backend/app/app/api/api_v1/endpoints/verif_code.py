import logging

from fastapi import APIRouter, Depends, Header, Body, File, UploadFile


from app.core.greensms import verif_code
from app.schemas.verif_code import VerifCodeCreate, VerifCodeSaveOnBase, VerifCodeGet
from app.core.response import SingleEntityResponse
from app.crud.crud_verif_code import verif_codes_service as service

from app.api import deps

router = APIRouter()


@router.post('/verification-codes/', response_model=SingleEntityResponse[VerifCodeGet],
             name='Получить код верификации',
             description='Получить код верификации, используя телефонный номер')
def create_verif_code(
    tel_for_greensms: VerifCodeCreate,
    # service: VerifCodesServices = Depends(),
    session=Depends(deps.get_db)
):
    code = verif_code(tel_for_greensms.tel)
    case_for_save = VerifCodeSaveOnBase(value=code, tel=tel_for_greensms.tel)
    service.create(db=session, obj_in=case_for_save)

    return SingleEntityResponse(data=VerifCodeGet(code=code))


if __name__ == "__main":
    logging.info('Running...')
