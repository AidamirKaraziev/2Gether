from app.crud.base import CRUDBase
from app.models import PartnerCompetence
from app.schemas.partner_competence import PartnerCompetenceCreate, PartnerCompetenceUpdate


class CrudPartnerCompetence(CRUDBase[PartnerCompetence, PartnerCompetenceCreate, PartnerCompetenceUpdate]):
    pass


crud_partner_competence = CrudPartnerCompetence(PartnerCompetence)
