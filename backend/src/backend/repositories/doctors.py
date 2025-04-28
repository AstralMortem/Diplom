from typing import Protocol
import uuid
from backend.core import get_session
from fastapi import Depends
from sqlalchemy import select, or_
from backend.models.users import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from .base import SQLCRUDRepository, ICRUDRepository


class IDoctorRepository(ICRUDRepository[Doctor, uuid.UUID]):
    async def get_doctor_for_login(self, username: str) -> Doctor | None:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Doctor | None:
        raise NotImplementedError

    async def get_by_phone_number(self, phone_number: str) -> Doctor | None:
        raise NotImplementedError


class SQLDoctorRepository(IDoctorRepository, SQLCRUDRepository[Doctor, uuid.UUID]):
    model = Doctor

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_doctor_for_login(self, username: str) -> Doctor | None:
        query = (
            select(self.model)
            .where(
                or_(self.model.email == username, self.model.phone_number == username)
            )
            .limit(1)
        )
        return await self.session.scalar(query)
    
    async def get_by_email(self, email: str) -> Doctor | None:
        query = select(self.model).where(self.model.email == email)
        return await self.session.scalar(query)
    
    async def get_by_phone_number(self, phone_number: str) -> Doctor | None:
        query = select(self.model).where(self.model.phone_number == phone_number)
        return await self.session.scalar(query)


async def get_doctor_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLDoctorRepository:
    return SQLDoctorRepository(session)
