from pydantic import BaseModel, Field


class ActivitySphereOfProjectCreate(BaseModel):
    project_id: int = Field(None, title="id проекта")
    activity_of_sphere_id: int = Field(None, title="id сферы деятельности")


class ActivitySphereOfProject(BaseModel):
    id: int = Field(None, title="id")
    project_id: int = Field(None, title="id проекта")
    activity_of_sphere_id: int = Field(None, title="id сферы деятельности")


class ActivitySphereOfProjectUpdate(BaseModel):
    pass
