import uuid
from backend.schemas import MedRecordCreate, MedRecordDetailRead, MedRecordRead, MedRecordUpdate
from backend.schemas.filters import MedRecordFilter
from backend.schemas.transcriptions import TranscriptionCreate, TranscriptionDetailRead, TranscriptionRead
from backend.utils.cbv import Controller
from backend.services.records import get_medical_record_service, MedRecordService
from fastapi import Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params


class MedRecordController(Controller):
    prefix = "/med-records"
    resource = "med-records"
    tags = ["MedRecords"]

    service: MedRecordService = Depends(get_medical_record_service)

    @Controller.get("/{record_id}", response_model=MedRecordDetailRead)
    async def get_record(self, record_id: uuid.UUID):
        """
        Get a medical record by ID.
        """
        return await self.service.get_by_id(record_id)
    
    @Controller.post("/", response_model=MedRecordRead)
    async def create_record(self, payload: MedRecordCreate):
        """
        Create a new medical record.
        """
        return await self.service.create(payload)
    
    @Controller.patch("/{record_id}", response_model=MedRecordRead)
    async def update_record(self, record_id: uuid.UUID, payload: MedRecordUpdate):
        """
        Update a medical record.
        """
        return await self.service.patch(record_id, payload)
    
    @Controller.delete("/{record_id}")
    async def delete_record(self, record_id: uuid.UUID):
        """
        Delete a medical record.
        """
        return await self.service.delete(record_id)

    @Controller.get("/", response_model=Page[MedRecordRead])
    async def list_records(self, pagination: Params = Depends(), filter: MedRecordFilter = FilterDepends(MedRecordFilter)):
        return await self.service.list(pagination, filter, set())
    
    
    @Controller.get("/{record_id}/transcriptions", response_model=Page[TranscriptionRead])
    async def list_transcriptions(self, record_id: uuid.UUID, pagination: Params = Depends()):
        return await self.service.get_transcriptions(record_id, pagination)
    
    @Controller.get("/{record_id}/transcriptions/{transcription_id}", response_model=TranscriptionDetailRead)
    async def get_transcription(self, record_id: uuid.UUID, transcription_id: int):
        return await self.service.get_transcription(record_id, transcription_id)
    
    @Controller.post("/{record_id}/transcriptions", response_model=TranscriptionRead)
    async def create_transcription(self, record_id: uuid.UUID, payload: TranscriptionCreate):
        return await self.service.create_transcription(record_id, payload)
    
    @Controller.delete("/{record_id}/transcriptions/{transcription_id}")
    async def delete_transcription(self, record_id: uuid.UUID, transcription_id: int):
        return await self.service.delete_transcription(record_id, transcription_id)
    