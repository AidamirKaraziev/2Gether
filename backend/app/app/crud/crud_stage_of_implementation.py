from typing import Optional

from app.crud.base import CRUDBase
from app.models import StageOfImplementation
from app.schemas.stage_of_implementation import StageOfImplementationCreate, StageOfImplementationUpdate
from sqlalchemy.orm import Session


class CrudStageOfImplementation(CRUDBase[StageOfImplementation,
                                         StageOfImplementationCreate,
                                         StageOfImplementationUpdate]):

    def update_location(self, db: Session, *, new_data: Optional[StageOfImplementationUpdate],
                        id: int):
        # проверить есть ли город с таким id
        if db.query(StageOfImplementation).filter(StageOfImplementation.id == id).first() is None:
            return None, -1, None
        this_implementation_stages = (db.query(
            StageOfImplementation).filter(StageOfImplementation.id == id).first())

        # Check_name
        if this_implementation_stages.name != new_data.name:
            if db.query(StageOfImplementation).filter(StageOfImplementation.name == new_data.name).first() is not None:
                return None, -2, None

        # Вот тут должно быть обновление базы данных
        db_obj = super().update(db=db, db_obj=this_implementation_stages, obj_in=new_data)
        return db_obj, 0, None


crud_stage_of_implementation = CrudStageOfImplementation(StageOfImplementation)
