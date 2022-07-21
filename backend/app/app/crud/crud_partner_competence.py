from typing import Optional

from app.crud.base import CRUDBase
from app.models import PartnerCompetence
from app.schemas.partner_competence import PartnerCompetenceCreate, PartnerCompetenceUpdate
from sqlalchemy.orm import Session


class CrudPartnerCompetence(CRUDBase[PartnerCompetence, PartnerCompetenceCreate, PartnerCompetenceUpdate]):
    def update_partner_competences(self, db: Session, *, new_data: Optional[PartnerCompetenceUpdate],
                        id: int):
        # проверить есть ли город с таким id
        if db.query(PartnerCompetence).filter(PartnerCompetence.id == id).first() is None:
            return None, -1, None
        this_object = (db.query(
            PartnerCompetence).filter(PartnerCompetence.id == id).first())

        # Check_name
        if this_object.name != new_data.name:
            if db.query(PartnerCompetence).filter(PartnerCompetence.name == new_data.name).first() is not None:
                return None, -2, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_object, obj_in=new_data)
        return db_obj, 0, None


crud_partner_competence = CrudPartnerCompetence(PartnerCompetence)
