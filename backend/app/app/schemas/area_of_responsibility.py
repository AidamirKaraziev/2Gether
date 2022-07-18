from pydantic import BaseModel, Field


class AreaOfResponsibilityCreate(BaseModel):
    name: str = Field(..., title="Название зоны ответственности")


class AreaOfResponsibilityUpdate(BaseModel):
    name: str = Field(..., title="Название зоны ответственности")


class AreaOfResponsibilityGet(BaseModel):
    id: int = Field(..., title="Идентификатор зоны ответственности")
    name: str = Field(..., title="Название зоны ответственности")
