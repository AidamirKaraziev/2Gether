from mimetypes import guess_type
from os.path import isfile
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.params import Path
from fastapi import Response, Request

from app.api import deps
from app.core.response import SingleEntityResponse
from app.crud.crud_project import crud_project
from app.exceptions import UnfoundEntity
from app.schemas.project import ProjectCreate, ProjectBase, ProjectPhoto

router = APIRouter()


@router.post('/project/',
             response_model=SingleEntityResponse[ProjectBase],
             name='Создать проект',
             description='Создать проект, ',
             tags=['Данные проекта']
             )
def update_user(

        new_data: ProjectCreate,
        session=Depends(deps.get_db),
):
    pass


@router.put("/project/photo/{num}",
            response_model=SingleEntityResponse[ProjectPhoto],
            name='Изменить фотографию',
            description='Изменить фотографию в проекте, если отправить пустой файл сбрасывает фото в проекте',
            tags=['Данные проекта'],
            )
def create_upload_file(
        request: Request,
        num: str = Path(...),
        file: Optional[UploadFile] = File(None),
        # current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
        ):
    if num not in ["main", "1", "2"]:
        raise UnfoundEntity(
            message="Неправильный num",
            num=2,
            description="Введите правильный num",
            path="$.body",
        )

    # user_id = current_user.id
    save_path = crud_project.adding_photo(num=num, file=file)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    return SingleEntityResponse(data=save_path)


@router.get("/static/{filename:path}", name='Получить статический файл', tags=['Инструменты'])
async def get_site(filename):
    filename = 'static/' + filename
    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, 'rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)

# Когда выводим user_id нужно ли выводить данные пользователя
# При сохранении фотографий проекта на сервере, 
#
#
