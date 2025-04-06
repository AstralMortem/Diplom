

from backend.models.users import Permission, Role
from backend.repositories.rbac import IPermissionRepository, IRoleRepository, get_permission_repository, get_role_repository
from backend.schemas.rbac import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate
from backend.core.exceptions import MedServiceException, status
from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_filter.base.filter import BaseFilterModel


class RBACService:

    def __init__(self, role_repository: IRoleRepository, permission_repository: IPermissionRepository):
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    async def create_role(self, role: RoleCreate, **kwargs):
        dump = role.model_dump(exclude_unset=True, exclude_none=True)
        if permissions := dump.pop("permissions", None):
            dump["permissions"] = await self.permission_repository.bulk_create(permissions)
        return await self.role_repository.create(dump, **kwargs)
    
    async def get_role(self, role_id: int, **kwargs):
        instance = await self.role_repository.get_by_id(role_id)
        if instance is None:
            raise MedServiceException(status.HTTP_404_NOT_FOUND, "Role not found", f"Role with id {role_id} not found")
        return instance
    
    async def delete_role(self, role_id: int, **kwargs):
        instance = await self.get_role(role_id, **kwargs)
        await self.role_repository.delete(instance, **kwargs)

    async def patch_role(self, role_id: int, role: RoleUpdate, **kwargs):
        instance = await self.get_role(role_id, **kwargs)
        dump = role.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
        return await self.role_repository.update(instance, dump, **kwargs)
    
    async def list_roles(self, pagination_params: Params, filter: BaseFilterModel | None = None, joins: set[str] | None = None, **kwargs) -> Page[Role]:
        return await self.role_repository.get_all(pagination_params, filter, joins, **kwargs)

    async def create_permission(self, permission: PermissionCreate, **kwargs):
        return await self.permission_repository.create(permission.model_dump(exclude_unset=True, exclude_none=True), **kwargs)
    
    async def get_permission(self, permission_id: int, **kwargs):
        instance = await self.permission_repository.get_by_id(permission_id, **kwargs)
        if instance is None:
            raise MedServiceException(status.HTTP_404_NOT_FOUND, "Permission not found", f"Permission with id {permission_id} not found")
        return instance
    
    async def delete_permission(self, permission_id: int, **kwargs):
        instance = await self.get_permission(permission_id, **kwargs)
        await self.permission_repository.delete(instance, **kwargs)

    async def patch_permission(self, permission_id: int, permission: PermissionUpdate, **kwargs):
        instance = await self.get_permission(permission_id, **kwargs)
        dump = permission.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)
        return await self.permission_repository.update(instance, dump, **kwargs)
    
    async def list_permissions(self, pagination_params: Params, filter: BaseFilterModel | None = None, joins: set[str] | None = None, **kwargs) -> Page[Permission]:
        return await self.permission_repository.get_all(pagination_params, filter, joins, **kwargs)
    
        
async def get_rbac_service(role_repository: IRoleRepository = Depends(get_role_repository), permission_repository: IPermissionRepository = Depends(get_permission_repository)):
    return RBACService(role_repository, permission_repository)
