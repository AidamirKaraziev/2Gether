from app.crud.base import CRUDBase
from app.models.area_of_responsibility import AreaOfResponsibility
from app.schemas.area_of_responsibility import AreaOfResponsibilityCreate, AreaOfResponsibilityUpdate


class CrudAreaOfResponsibility(CRUDBase[AreaOfResponsibility, AreaOfResponsibilityCreate, AreaOfResponsibilityUpdate]):
    pass


crud_area_of_responsibility = CrudAreaOfResponsibility(AreaOfResponsibility)
