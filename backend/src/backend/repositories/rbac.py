from backend.core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .base import ICRUDRepository, SQLCRUDRepository
from backend.models.users import Role, Permission


class IRoleRepository(ICRUDRepository[Role, int]):
    model = Role

class IPermissionRepository(ICRUDRepository[Permission, int]):
    model = Permission


class RoleRepository(IRoleRepository, SQLCRUDRepository[Role, int]):
    pass

class PermissionRepository(IPermissionRepository, SQLCRUDRepository[Permission, int]):
    pass



async def get_role_repository(session: AsyncSession = Depends(get_session)):
    return RoleRepository(session)

async def get_permission_repository(session: AsyncSession = Depends(get_session)):
    return PermissionRepository(session)


