from app.models import Location

from app.schemas.location import LocationGet


def get_location(db_obj: Location) -> LocationGet:
    return LocationGet(
        id=db_obj.id,
        name=db_obj.name
    )

# def get_location_id(id: int) -> LocationGet:
#     loc =
#     return