from backend.core.db import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, DateTime, ForeignKey, Date, Integer, Text, String, JSON, Boolean
from datetime import date, datetime
import uuid

from backend.models.users import Doctor, Patient, Department


class RecordTranscription(Model):
    __tablename__ = "medical_record_transcriptions"

    transcription_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.record_id"), primary_key=True
    )

    audio_url: Mapped[str] = mapped_column(Text)
    audio_duration: Mapped[int] = mapped_column(Integer)
    transcription_text: Mapped[str] = mapped_column(Text)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Metadata
    asr_model: Mapped[str] = mapped_column(String(100))
    asr_config: Mapped[dict] = mapped_column(JSON)
    language: Mapped[str] = mapped_column(String(2), default="uk")

    medical_record: Mapped["MedicalRecord"] = relationship(back_populates="transcriptions")


class MedicalRecord(Model):
    __tablename__ = "medical_records"

    record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.patient_id"))
    doctor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("doctors.doctor_id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.department_id"))
    examination_date: Mapped[datetime] = mapped_column(DateTime)

    patient: Mapped[Patient] = relationship(lazy="joined", back_populates="medical_records", viewonly=True)
    doctor: Mapped[Doctor] = relationship(lazy="joined", back_populates="medical_records", viewonly=True)
    transcriptions: Mapped[list[RecordTranscription]] = relationship(lazy="joined", back_populates="medical_record")
    department: Mapped[Department] = relationship(lazy="joined")
