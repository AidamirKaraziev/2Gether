from app.models import PartnerCompetence
from app.schemas.partner_competence import PartnerCompetenceGet


def get_partner_competence(db_obj: PartnerCompetence) -> PartnerCompetenceGet:
    return PartnerCompetenceGet(
        id=db_obj.id,
        name=db_obj.name
    )
