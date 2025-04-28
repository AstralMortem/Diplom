
from backend.schemas.base import Schema
from datetime import datetime

class DepartmentRead(Schema):
    department_id: int
    name: str
    description: str | None = None
    contact_phone: str | None = None

    created_at: datetime
    updated_at: datetime


class DepartmentCreate(Schema):
    name: str
    description: str | None = None
    contact_phone: str | None = None


class DepartmentUpdate(Schema):
    name: str | None = None
    description: str | None = None
    contact_phone: str | None = None

