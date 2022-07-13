from fastapi import APIRouter

from app.api.api_v1.endpoints import entrance, verif_code, users, \
    location, stage_of_implementation, partner_competence, activity_sphere, project


api_router = APIRouter()


api_router.include_router(entrance.router, tags=["Вход"])
api_router.include_router(verif_code.router, tags=["Вход"])
api_router.include_router(users.router)
api_router.include_router(location.router)
api_router.include_router(stage_of_implementation.router)
api_router.include_router(partner_competence.router)
api_router.include_router(activity_sphere.router)
api_router.include_router(project.router)
