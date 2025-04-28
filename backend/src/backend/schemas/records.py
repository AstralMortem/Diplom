import uuid
from backend.schemas.departments import DepartmentRead
from .base import Schema
from datetime import datetime

from .users import PatientRead, DoctorRead
from .transcriptions import TranscriptionRead

class MedRecordCreate(Schema):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    department_id: int
    examination_date: datetime

class MedRecordRead(MedRecordCreate):
    record_id: uuid.UUID
    patient: PatientRead
    doctor: DoctorRead
    department: DepartmentRead
    created_at: datetime
    updated_at: datetime


class MedRecordDetailRead(MedRecordRead):
    transcriptions: list[TranscriptionRead] = []

class MedRecordUpdate(Schema):
    patient_id: uuid.UUID | None = None
    department_id: int | None = None
    examination_date: datetime | None = None


