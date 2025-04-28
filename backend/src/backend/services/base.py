from backend.repositories.base import ICRUDRepository, ID, M
from typing import Any, Coroutine, Generic, TypeVar
from backend.core.exceptions import MedServiceException,status
from backend.schemas.base import Schema
from fastapi_pagination import Params, Page
from fastapi_filter.base.filter import BaseFilterModel
from sqlalchemy.exc import IntegrityError


class CRUDService(Generic[M, ID]):
    def __init__(self, repo: ICRUDRepository[M, ID]):
        self.repo = repo
    
    def not_found_error(self,code: int = 404, title: str = "Item not found", description: str | None = "Item not found", debug: Exception | None = None) -> MedServiceException:
        return MedServiceException(code, title, description, debug)
    
    async def get_by_id(self, id: ID) -> M:
        instance = await self.repo.get_by_id(id)
        if instance is None:
            raise self.not_found_error()
        return instance
    
    async def create(self, payload: Schema) -> M:
        dump = payload.model_dump(exclude_unset=True)
        return await self.repo.create(dump)
    
    async def patch(self, id: ID, payload: Schema) -> M:
        instance = await self.get_by_id(id)
        dump = payload.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True)
        return await self.repo.update(instance, dump)
    
    async def delete(self, id: ID):
        instance = await self.get_by_id(id)
        return await self.repo.delete(instance)
    
    async def list(self, pagination: Params, filter: BaseFilterModel | None = None, joins: set[str] | None = None, **kwargs) -> Page[M]:
        return await self.repo.get_all(pagination, filter, joins, **kwargs)
