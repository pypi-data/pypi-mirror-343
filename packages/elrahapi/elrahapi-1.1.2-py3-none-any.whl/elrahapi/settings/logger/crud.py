from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from ..database import session_manager
from .model import Logger
from .schema import LogPydanticModel
log_crud_models = CrudModels (
    entity_name='log',
    primary_key_name='id',
    SQLAlchemyModel=Logger,
    PydanticModel=LogPydanticModel
)
logCrud = CrudForgery(
    session_manager=session_manager,
    crud_models=log_crud_models
)
