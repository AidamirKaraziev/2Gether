from app.models.area_of_responsibility import AreaOfResponsibility
from app.schemas.area_of_responsibility import AreaOfResponsibilityGet


def get_area_of_responsibility(db_obj: AreaOfResponsibility) -> AreaOfResponsibilityGet:
    return AreaOfResponsibilityGet(
        id=db_obj.id,
        name=db_obj.name
    )
