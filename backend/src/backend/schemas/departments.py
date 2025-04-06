
from backend.schemas.base import Schema


class DepartmentRead(Schema):
    department_id: int
    name: str
    description: str | None = None
    contact_phone: str | None = None


class DepartmentCreate(Schema):
    name: str
    description: str | None = None
    contact_phone: str | None = None


class DepartmentUpdate(Schema):
    name: str | None = None
    description: str | None = None
    contact_phone: str | None = None

