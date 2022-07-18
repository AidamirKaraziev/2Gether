from app.getters.area_of_responsibility import get_area_of_responsibility
from app.getters.location import get_location
from app.models.moderator import Moderator
from app.schemas.moderator import ModeratorBase

from app.schemas.moderator import ModeratorGet


def get_moderator(moderator: Moderator) -> ModeratorGet:
    return ModeratorGet(
        id=moderator.id,
        login=moderator.login,
        password=moderator.password,
        tel=moderator.tel,
        first_name=moderator.first_name,
        last_name=moderator.last_name,
        birthday=moderator.birthday,
        location=get_location(moderator.location) if moderator.location is not None else None,
        closed_appeals=moderator.closed_appeals,
        open_appeals=moderator.open_appeals,
        photo=moderator.photo,
        area_of_responsibility=get_area_of_responsibility(
            moderator.area_of_responsibility) if moderator.area_of_responsibility is not None else None,
        average_first_response_time=moderator.average_first_response_time,
        is_superuser=moderator.is_superuser
    )
