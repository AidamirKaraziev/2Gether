from mimetypes import guess_type
from os.path import isfile
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Header
from fastapi.params import Path
from fastapi import Response, Request

from app.api import deps
from app.core.response import SingleEntityResponse
from app.crud.crud_project import crud_project
from app.exceptions import UnfoundEntity
from app.schemas.project import ProjectCreate, ProjectBase, ProjectPhoto, ProjectGet
from app.getters.project import get_project_photo, get_project


router = APIRouter()


@router.post('/project/',
             response_model=SingleEntityResponse[ProjectGet],
             name='Создать проект',
             description='Создать проект, ',
             tags=['Данные проекта']
             )
def create_project(
        new_data: ProjectCreate,
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    # Что-то правильное, пример Володи
    # crud_project.create_for_user(db=session, obj_in=new_data, user_field_value=current_user)

    project, competence_project, activity_project = crud_project.create_project(db=session, project=new_data,
                                                                                user_id=current_user.id)
    data = get_project(project=project)

    # return SingleEntityResponse(data=get_project(current_user, request=request))
    return SingleEntityResponse(data=data)


# Добавление фото проекта, загрузка их на сервер, возвращение ссылок на фото
@router.put("/project/photo/{num}",
            response_model=SingleEntityResponse[ProjectPhoto],
            name='Добавляет фотографию',
            description='Добавляет фотографию в проекте',
            tags=['Данные проекта'],
            )
def create_upload_file(
        request: Request,
        file: Optional[UploadFile] = File(None),
        # current_user=Depends(deps.get_current_user_by_bearer),
        # session=Depends(deps.get_db),
        ):

    save_path = crud_project.adding_photo(file=file)
    if not save_path:
        raise UnfoundEntity(message="Не отправлен загружаемый файл",
                            num=2,
                            description="Попробуйте загрузить файл еще раз",
                            path="$.body",
                            )
    response = get_project_photo(path_name=save_path, request=request, )
    return SingleEntityResponse(data=response)


@router.get("/static/{filename:path}", name='Получить статический файл', tags=['Инструменты'])
async def get_site(filename):
    filename = 'static/' + filename
    if not isfile(filename):
        return Response(status_code=404)

    with open(filename, 'rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


# """GET API PROJECT"""
@router.get('/project/',
            response_model=SingleEntityResponse[ProjectGet],
            name='Получить данные проекта',
            description='Получение всех  данных проекта, по токену',
            tags=['Данные проекта']
            )
def get_data(
        project_id: Optional[int] = Header(None),
        session=Depends(deps.get_db),
):
    project = crud_project.get(db=session, id=project_id)
    return SingleEntityResponse(data=get_project(project=project))


# Когда выводим user_id нужно ли выводить данные пользователя
# При сохранении фотографий проекта на сервере, 
#
#
