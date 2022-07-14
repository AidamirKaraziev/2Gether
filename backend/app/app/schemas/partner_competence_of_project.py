from pydantic import BaseModel, Field


class PartnerCompetenceOfProjectCreate(BaseModel):
    project_id: int = Field(..., title="id проекта")
    partner_competence_id: int = Field(..., title="id компетенции")

#
# class PartnerCompetenceGet(BaseModel):
#     name: str = Field(..., title="Название компетенции")
