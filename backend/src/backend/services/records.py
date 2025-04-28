import uuid
from backend.repositories.transcriptions import ITranscriptionRepository, get_transcription_repository
from backend.schemas.filters import TranscriptionFilter
from backend.schemas.transcriptions import TranscriptionCreate
from fastapi import Depends, HTTPException
from fastapi_pagination import Params
from .base import CRUDService
from backend.repositories.records import IRecordRepository, get_medical_record_repository
from backend.models.med_records import MedicalRecord

class MedRecordService(CRUDService[MedicalRecord, uuid.UUID]):

    def __init__(self, repo: IRecordRepository, transcription_repo: ITranscriptionRepository):
        super().__init__(repo)
        self.transcription_repo = transcription_repo

    async def get_transcription(self, record_id: uuid.UUID, transcription_id: int):
        instance = await self.transcription_repo.get_by_id(record_id, transcription_id)
        if instance is None:
            raise HTTPException(status_code=404, detail="Transcription not found")
        return instance
    
    async def get_transcriptions(self,record_id: uuid.UUID, params: Params):
        filter = TranscriptionFilter(record_id=record_id)
        return await self.transcription_repo.get_all(params, filter, set())
    
    async def create_transcription(self, record_id: uuid.UUID, payload: TranscriptionCreate):
        payload.record_id = record_id
        instance = await self.transcription_repo.create(payload.model_dump())
        return instance
    
    async def delete_transcription(self, record_id: uuid.UUID, transcription_id: int):
        instance = await self.get_transcription(record_id, transcription_id)
        return await self.transcription_repo.delete(instance)


async def get_medical_record_service(
    repo: IRecordRepository = Depends(get_medical_record_repository),
    transcription_repo: ITranscriptionRepository = Depends(get_transcription_repository)
):
    return MedRecordService(repo, transcription_repo)