from typing import TYPE_CHECKING
import uuid

from pydantic import ConfigDict, Field
from .departments import DepartmentRead

from .rbac import RoleRead
from .base import Schema
from .auth import Gender
from uuid import UUID
from datetime import date, datetime

if TYPE_CHECKING:
    from .records import MedRecordRead


class DoctorRead(Schema):
    doctor_id: UUID
    first_name: str
    last_name: str
    middle_name: str
    email: str
    phone_number: str
    birth_data: date
    is_active: bool
    gender: Gender
    specialization: str
    department: DepartmentRead | None = None
    created_at: datetime
    updated_at: datetime

    

class DoctorDetailRead(DoctorRead):
    role: RoleRead
    patients: list["PatientRead"]


class DoctorUpdate(Schema):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    birth_data: date | None = None
    gender: Gender | None = None
    specialization: str | None = None
    department_id: int | None = None
    role_id: int | None = None
    password: str | None = None

class DoctorCreate(Schema):
    first_name: str
    last_name: str
    middle_name: str
    email: str
    phone_number: str
    birth_data: date
    gender: Gender
    specialization: str
    department_id: int | None = None
    role_id: int | None = None
    password: str


class MedRecordInPatient(Schema):
    record_id: uuid.UUID
    examination_date: datetime
    doctor: DoctorRead
    department: DepartmentRead

class PatientRead(Schema):
    patient_id: uuid.UUID
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str
    email: str | None
    birth_data: date
    is_active: bool
    created_at: datetime
    updated_at: datetime



class PatientDetailRead(PatientRead):
    address: str
    gender: Gender
    # medical_records: list[MedRecordInPatient] = []

class PatientCreate(Schema):
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str
    email: str | None = None
    address: str
    birth_data: date
    gender: Gender


class PatientUpdate(Schema):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None
    birth_data: date | None = None
    gender: Gender | None = None


class DepartmentDetailRead(DepartmentRead):
    doctors: list[DoctorRead] = []