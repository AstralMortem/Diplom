from backend.core.db import get_session
from backend.models.users import Patient
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .base import ICRUDRepository, SQLCRUDRepository
import uuid


class IPatientRepository(ICRUDRepository[Patient, uuid.UUID]):
    async def get_by_email(self, email: str) -> Patient | None:
        raise NotImplementedError

    async def get_by_phone_number(self, phone_number: str) -> Patient | None:
        raise NotImplementedError


class SQLPatientRepository(IPatientRepository, SQLCRUDRepository[Patient, uuid.UUID]):
    model = Patient

    async def get_by_phone_number(self, phone_number: str) -> Patient | None:
        return await self.get_by_field('phone_number', phone_number)
    
    async def get_by_email(self, email: str) -> Patient | None:
        return await self.get_by_field('email', email)


def get_patient_repository(session: AsyncSession = Depends(get_session)):
    return SQLPatientRepository(session)
