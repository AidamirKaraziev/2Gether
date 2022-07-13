from app.models import StageOfImplementation
from app.schemas.stage_of_implementation import StageOfImplementationGet


def get_stage_of_implementation(db_obj: StageOfImplementation) -> StageOfImplementationGet:
    return StageOfImplementationGet(
        id=db_obj.id,
        name=db_obj.name
    )
