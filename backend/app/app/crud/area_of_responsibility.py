from typing import Optional

from app.crud.base import CRUDBase
from app.models.area_of_responsibility import AreaOfResponsibility
from app.schemas.area_of_responsibility import AreaOfResponsibilityCreate, AreaOfResponsibilityUpdate
from sqlalchemy.orm import Session


class CrudAreaOfResponsibility(CRUDBase[AreaOfResponsibility, AreaOfResponsibilityCreate, AreaOfResponsibilityUpdate]):
    def update_responsibility_area(self, db: Session, *, new_data: Optional[AreaOfResponsibilityUpdate],
                                id: int):
        # проверить есть ли сфера с таким id
        this_object = (db.query(
            AreaOfResponsibility).filter(AreaOfResponsibility.id == id).first())
        if this_object is None:
            return None, -1, None

        # Check_name
        if this_object.name != new_data.name:
            if db.query(AreaOfResponsibility).filter(AreaOfResponsibility.name == new_data.name).first() is not None:
                return None, -2, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_object, obj_in=new_data)
        return db_obj, 0, None


crud_area_of_responsibility = CrudAreaOfResponsibility(AreaOfResponsibility)
