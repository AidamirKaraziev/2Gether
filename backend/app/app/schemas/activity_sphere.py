from typing import Optional

from pydantic import BaseModel, Field


class ActivitySphereCreate(BaseModel):
    name: str = Field(..., title="Название сферы деятельности")


class ActivitySpherePictureCreate(BaseModel):
    name: str = Field(..., title="Название сферы деятельности")
    picture: str = Field(..., title="путь к папке с SVG иконкой")


class ActivitySphereUpdate(BaseModel):
    name: str = Field(..., title="Название сферы деятельности")


class ActivitySphereGet(BaseModel):
    id: int = Field(..., title="Идентификатор сферы деятельности")
    name: str = Field(..., title="Название сферы деятельности")
    picture: Optional[str] = Field(..., title="путь к папке с SVG иконкой")


class ActivitySpherePicture(BaseModel):
    picture: str = Field(..., title="путь к папке с SVG иконкой")
