from app.crud.base import CRUDBase
from app.models import PartnerCompetence
from app.schemas.partner_competence import PartnerCompetenceCreate, PartnerCompetenceUpdate
from sqlalchemy.orm import Session


class CrudPartnerCompetence(CRUDBase[PartnerCompetence, PartnerCompetenceCreate, PartnerCompetenceUpdate]):
    pass


crud_partner_competence = CrudPartnerCompetence(PartnerCompetence)
