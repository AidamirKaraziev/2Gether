from pydantic import BaseModel, Field


class PartnerCompetenceCreate(BaseModel):
    name: str = Field(..., title="Название компетенции")


class PartnerCompetenceUpdate(BaseModel):
    name: str = Field(..., title="Название компетенции")


class PartnerCompetenceGet(BaseModel):
    id: int = Field(..., title="Идентификатор компетенции")
    name: str = Field(..., title="Название компетенции")
