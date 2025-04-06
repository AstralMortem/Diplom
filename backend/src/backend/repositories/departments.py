from backend.core.db import get_session
from backend.models.users import Department
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .base import ICRUDRepository, SQLCRUDRepository

class IDepartmentRepository(ICRUDRepository[Department, int]):
    model = Department

class DepartmentRepository(IDepartmentRepository, SQLCRUDRepository[Department, int]):
    pass


async def get_department_repository(session: AsyncSession = Depends(get_session)) -> DepartmentRepository:
    return DepartmentRepository(session)
