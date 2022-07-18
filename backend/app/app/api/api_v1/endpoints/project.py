import logging
from mimetypes import guess_type
from os.path import isfile
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Header, Query
from fastapi.params import Path
from fastapi import Response, Request

from app.api import deps
from app.core.response import SingleEntityResponse
from app.crud.crud_project import crud_project
from app.exceptions import UnfoundEntity
from app.schemas.project import ProjectCreate, ProjectBase, ProjectPhoto, ProjectGet
from app.getters.project import get_project_photo, get_project

from app.exceptions import UnprocessableEntity

from app.core.response import ListOfEntityResponse, Meta

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

    project, code, indexes = crud_project.create_project(db=session, project=new_data, user_id=current_user.id)

    # обработка исключений того что вернул
    if code == -1:
        raise UnprocessableEntity(
            message="Проект с таким именем уже есть",
            num=2,
            description="поменяйте имя проекта",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Нет такого пользователя",
            num=3,
            description="Попробуйте зайти заново",
            path="$.body",
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Нет такого города!",
            num=4,
            description="Попробуйте выбрать город еще раз!",
            path="$.body"
        )
    if code == -4:
        raise UnprocessableEntity(
            message="Нет такой сферы деятельности",
            num=5,
            description="Попробуйте выбрать сферу деятельности заново!",
            path="$.body"
        )

    if code == -5:
        raise UnprocessableEntity(
            message="Нет такой стадии реализации!",
            num=6,
            description="Попробуйте выбрать стадию реализации еще раз!",
            path="$.body"
        )
    if code == -6:
        raise UnprocessableEntity(
            message="Нет таких компетенций!",
            num=7,
            description="Попробуйте выбрать компетенции партнера еще раз!",
            path="$.body"
        )

    return SingleEntityResponse(data=get_project(project=project))


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
@router.get('/project/{project_id}/',
            response_model=SingleEntityResponse[ProjectGet],
            name='Получить данные проекта',
            description='Получение всех  данных проекта, по токену',
            tags=['Данные проекта']
            )
def get_data(
        project_id: int = Path(..., title='Id проекта'),
        session=Depends(deps.get_db),
):
    project = crud_project.get(db=session, id=project_id)
    if project is None:
        raise UnprocessableEntity(
            message="Такого проекта не обнаружено!",
            num=1,
            description="Попробуйте еще раз!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_project(project=project))


# Апи удаления Проекта ПОКА ЧТО НЕ РАБОТАЕТ, ПОТОМУ ЧТО ДЕВАЙСЫ МОРОСЯТ!!!!!
@router.delete("/project/{project_id}",
               response_model=SingleEntityResponse,
               name='Удаляет проект',
               description='Полностью удаляет проект',
               tags=['Данные проекта'])
def remove_with_path(
        project_id: int = Path(..., title='Id проекта'),
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db)
):
    # проверить принадлежит ли этот проект юзеру
    check_project = crud_project.getting(db=session, user_id=current_user.id, project_id=project_id)
    if check_project is not None:
        raise UnfoundEntity(message="Проект вам не принадлежит",
                            num=1,
                            description="Можете удалять только свои проекты",
                            path="$.body",
                            )

    return SingleEntityResponse(data=crud_project.remove(db=session, id=project_id))


# Вывод всех проектов пользователя
@router.get('/project/{user_id}',
            response_model=ListOfEntityResponse,
            name='Список проектов пользователя',
            description='Получение списка всех проектов данного пользователя',
            tags=['Инструменты']
            )
def get_data(
        user_id: int = Path(..., title='Id пользователя'),
        session=Depends(deps.get_db),
        # page: int = Query(1, title="Номер страницы")
):
    data = crud_project.get_multi_project(db=session, user_id=user_id)
    return ListOfEntityResponse(data=data)


# Изменить данные проекта
@router.put('/project/{project_id}',
            response_model=SingleEntityResponse[ProjectGet],
            name='Изменить данные проекта',
            description='Изменить данные текущего проекта',
            tags=['Данные проекта']
            )
def update_project(
        new_data: ProjectCreate,
        project_id: int = Path(..., title='Id проекта'),
        current_user=Depends(deps.get_current_user_by_bearer),
        session=Depends(deps.get_db),
):
    project, code, indexes = crud_project.update_project(db=session, project=new_data, user_id=current_user.id, project_id=project_id)
    if code == -1:
        raise UnprocessableEntity(
            message="Проект с таким именем уже есть",
            num=2,
            description="поменяйте имя проекта",
            path="$.body"
        )
    if code == -2:
        raise UnprocessableEntity(
            message="Нет такого пользователя",
            num=3,
            description="Попробуйте зайти заново",
            path="$.body",
        )
    if code == -3:
        raise UnprocessableEntity(
            message="Проект не принадлежит пользователю ",
            num=4,
            description="Попробуйте изменить свой проект ",
            path="$.body",
        )
    if code == -4:
        raise UnprocessableEntity(
            message="Нет такого города!",
            num=5,
            description="Попробуйте выбрать город еще раз!",
            path="$.body"
        )
    if code == -5:
        raise UnprocessableEntity(
            message="Нет такой сферы деятельности",
            num=6,
            description="Попробуйте выбрать сферу деятельности заново!",
            path="$.body"
        )

    if code == -6:
        raise UnprocessableEntity(
            message="Нет такой стадии реализации!",
            num=7,
            description="Попробуйте выбрать стадию реализации еще раз!",
            path="$.body"
        )
    if code == -7:
        raise UnprocessableEntity(
            message="Нет таких компетенций!",
            num=8,
            description="Попробуйте выбрать компетенции партнера еще раз!",
            path="$.body"
        )
    return SingleEntityResponse(data=get_project(project=project))


# Когда выводим project.user_id нужно ли выводить краткую информацию о пользователе?
# В апи по выводу всех проектов юзера, надо проверять есть ли такой юзер?
# Написать апи для добавления путей хранения картинок для сфер деятельности(АДМИНКА)
# Создание сфер деятельности Нужно написать в одной апи или в двух(+картинки)

# Нужно ли запрещать пользователям создавать проекты с пустыми названиями?
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNjU4NTY0MjE2LCJpYXQiOjE2NTc4NzMwMTYsIm5iZiI6MTY1Nzg3MzAxNiwianRpIjoiMTcxNjJjMjAtMWUxZC00ZjRiLWJjZGEtZTFmZGI2ZjM3NmNhIn0.iINXp1BASqZ0MCtC7ME2cQyy3YV1rbinM6V_nty17h8

if __name__ == "__main":
    logging.info('Running...')
