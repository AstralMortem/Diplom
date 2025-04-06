import uuid

from backend.core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .base import ICRUDRepository, SQLCRUDRepository
from backend.models.med_records import MedicalRecord

class IRecordRepository(ICRUDRepository[MedicalRecord, uuid.UUID]):
    model = MedicalRecord


class RecordRepository(IRecordRepository, SQLCRUDRepository[MedicalRecord, uuid.UUID]):
    pass


async def get_medical_record_repository(session: AsyncSession = Depends(get_session)):
    return RecordRepository(session)