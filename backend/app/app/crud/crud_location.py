from app.crud.base import CRUDBase
from app.models.location import Location
from app.schemas.location import LocationUpdate, LocationCreate


class CrudLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    pass


crud_location = CrudLocation(Location)
