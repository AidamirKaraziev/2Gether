from app.crud.base import CRUDBase
from app.models import StageOfImplementation
from app.schemas.stage_of_implementation import StageOfImplementationCreate, StageOfImplementationUpdate


class CrudStageOfImplementation(CRUDBase[StageOfImplementation,
                                         StageOfImplementationCreate,
                                         StageOfImplementationUpdate]):

    pass


crud_stage_of_implementation = CrudStageOfImplementation(StageOfImplementation)
