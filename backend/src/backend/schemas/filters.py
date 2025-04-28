from fastapi_filter.contrib.sqlalchemy import Filter
from backend.models.med_records import MedicalRecord, RecordTranscription
import uuid
from datetime import datetime


class MedRecordFilter(Filter):
    patient_id: uuid.UUID | None = None
    doctor_id: uuid.UUID | None = None
    department_id: int | None = None
    examination_date: datetime | None = None

    class Constants(Filter.Constants):
        model = MedicalRecord


class TranscriptionFilter(Filter):
    record_id: uuid.UUID | None = None

    class Constants(Filter.Constants):
        model = RecordTranscription

