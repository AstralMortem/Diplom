import uuid
from sqlalchemy import select
from backend.core.db import get_session
from .base import ICRUDRepository, SQLCRUDRepository
from backend.models.med_records import RecordTranscription
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


class ITranscriptionRepository(ICRUDRepository[RecordTranscription, int]):
    model = RecordTranscription

    async def get_by_id(self, record_id: uuid.UUID, transcription_id: int) -> RecordTranscription | None:
        raise NotImplementedError


class TranscriptionRepository(ITranscriptionRepository, SQLCRUDRepository[RecordTranscription, int]):
    
    async def get_by_id(self, record_id: uuid.UUID, transcription_id: int) -> RecordTranscription | None:
        qs = select(self.model).where(self.model.record_id == record_id, self.model.transcription_id == transcription_id)
        return await self.session.scalar(qs)


async def get_transcription_repository(session: AsyncSession = Depends(get_session)) -> ITranscriptionRepository:
    return TranscriptionRepository(session)
