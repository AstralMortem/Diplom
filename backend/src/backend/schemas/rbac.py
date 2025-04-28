from enum import StrEnum
from .base import Schema

class PermissionAction(StrEnum):
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DELETE = "delete"


class PermissionRead(Schema):
    permission_id: int
    resource: str
    action: PermissionAction | str 


class PermissionCreate(Schema):
    resource: str
    action: PermissionAction | str

class PermissionUpdate(Schema):
    resource: str | None = None
    action: PermissionAction | str | None = None


class RoleRead(Schema):
    role_id: int
    name: str
    permissions: list[PermissionRead] = []

class RoleCreate(Schema):
    name: str
    permissions: list[PermissionCreate] | None = None

class RoleUpdate(Schema):
    name: str | None = None
