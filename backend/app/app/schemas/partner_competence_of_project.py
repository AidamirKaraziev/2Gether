from pydantic import BaseModel, Field


class PartnerCompetenceOfProjectCreate(BaseModel):
    project_id: int = Field(None, title="id проекта")
    partner_competencies_id: int = Field(None, title="id компетенции")


class PartnerCompetenceOfProject(BaseModel):
    id: int = Field(None, title="id")
    project_id: int = Field(None, title="id проекта")
    partner_competencies_id: int = Field(None, title="id компетенции")


class PartnerCompetenceOfProjectUpdate(BaseModel):
    pass


# class PartnerCompetenceGet(BaseModel):
#     name: str = Field(..., title="Название компетенции")
