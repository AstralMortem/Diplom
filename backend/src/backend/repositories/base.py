from typing import Any, Coroutine, Protocol, TypeVar
import uuid
from backend.core import Model
from backend.core.exceptions import MedServiceException, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_filter.base.filter import BaseFilterModel
from fastapi_filter.contrib.sqlalchemy.filter import Filter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


M = TypeVar("M", bound=Model)
ID = TypeVar("ID", contravariant=True)


class ICRUDRepository(Protocol[M, ID]):
    model: type[M]

    async def get_by_id(self, id: ID) -> M | None:
        raise NotImplementedError
    
    async def get_by_field(self, field: str, value: Any) -> M | None:
        raise NotImplementedError

    async def create(self, payload: dict[str, Any]) -> M:
        raise NotImplementedError

    async def update(self, instance: M, payload: dict[str, Any]) -> M:
        raise NotImplementedError

    async def delete(self, instance: M) -> None:
        raise NotImplementedError

    async def get_all(self, pagination_params: Params, filter: BaseFilterModel | None = None, joins: set[str] | None= None, **kwargs: Any) -> Page[M]:
        raise NotImplementedError
    
    async def bulk_create(self, payloads: list[dict[str, Any]]) -> list[M]:
        raise NotImplementedError
    
    async def bulk_update(self, instances: list[M], payloads: list[dict[str, Any]]) -> list[M]:
        raise NotImplementedError


class SQLCRUDRepository(ICRUDRepository[M, ID]):
    model: type[M]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: ID) -> M | None:
        return await self.session.get(self.model, id)
     
    async def get_by_field(self, field: str, value: Any) -> M | None:
        query = select(self.model).where(getattr(self.model, field) == value)
        return await self.session.scalar(query)

    async def create(self, payload: dict[str, Any]) -> M:
        instance = self.model(**payload)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: M, payload: dict[str, Any]) -> M:
        self.session.add(instance)
        for key, value in payload.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: M) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def get_all(self, pagination_params: Params, filter: Filter | None = None, joins: set[str] | None= None, **kwargs: Any) -> Page[M]:
        query = select(self.model)
        if filter:
            print(joins)
            if joins is None:
                raise MedServiceException(status.HTTP_400_BAD_REQUEST, "Joins are required for filtering", "Yoy set filter model, but dont set joins", debug="create argument _'tablename'_join' in repository, then pass tablename in joins args, or set empty set")
            for join in joins:
                join_method = f"_{join}_join"
                if not hasattr(self, join_method):
                    raise MedServiceException(status.HTTP_400_BAD_REQUEST, "Join method not found", f"Join method {join_method} not found", debug=f"create method {join_method} in repository")
                func = getattr(self, join_method)
                query = func(query, **kwargs)
            query = filter.filter(query)

    
        return await paginate(self.session, query, pagination_params)
    

    async def bulk_create(self, payloads: list[dict[str, Any]]) -> list[M]:
        instances = [self.model(**payload) for payload in payloads]
        self.session.add_all(instances)
        await self.session.commit()
        return instances
    
    async def bulk_update(self, instances: list[M], payloads: list[dict[str, Any]]) -> list[M]:
        self.session.add_all(instances)
        for idx, instance in enumerate(instances):
            for key, value in payloads[idx].items():
                setattr(instance, key, value)
        await self.session.commit()
        return instances

