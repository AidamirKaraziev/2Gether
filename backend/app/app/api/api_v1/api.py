from fastapi import APIRouter

from app.api.api_v1.endpoints import entrance, verif_code, users, \
    location, stage_of_implementation, partner_competence, activity_sphere, project, area_of_responsibility, moderator


api_router = APIRouter()


api_router.include_router(entrance.router, tags=["Вход / Мобильное приложение"])
api_router.include_router(verif_code.router, tags=["Вход / Мобильное приложение"])
api_router.include_router(users.router)
# api_router.include_router(location.router, tags=['Мобильное приложение / Города'])
api_router.include_router(location.router, tags=['Админ панель / Города'])
api_router.include_router(stage_of_implementation.router, tags=['Админ панель / Стадии реализации'])
api_router.include_router(partner_competence.router, tags=['Админ панель / Партнерские компетенции'])
api_router.include_router(activity_sphere.router, tags=['Админ панель / Сферы деятельности'])
api_router.include_router(project.router)
api_router.include_router(area_of_responsibility.router, tags=['Админ панель / Зоны ответственности'])
api_router.include_router(moderator.router)
