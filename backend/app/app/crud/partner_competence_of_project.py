from app.crud.base import CRUDBase
from app.schemas.partner_competence_of_project import PartnerCompetenceOfProjectCreate,\
    PartnerCompetenceOfProjectUpdate

from app.models import PartnerCompetenceOfProject


class CrudPartnerCompetenceOfProject(CRUDBase[PartnerCompetenceOfProject, PartnerCompetenceOfProjectCreate,
                                              PartnerCompetenceOfProjectUpdate]):

    pass


crud_partner_competence_of_project = CrudPartnerCompetenceOfProject(PartnerCompetenceOfProject)
