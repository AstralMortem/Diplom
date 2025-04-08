from backend.schemas.rbac import RoleCreate, RoleRead, RoleUpdate, PermissionCreate, PermissionRead, PermissionUpdate
from backend.services.rbac import RBACService, get_rbac_service
from backend.utils.cbv import Controller
from fastapi import Depends
from fastapi_pagination import Page, Params
from backend.utils.permission_helper import HasPermission, PermissionAction

class RoleController(Controller):
    prefix = "/roles"
    resource = "roles"
    tags = ["Roles", "RBAC"]

    service: RBACService = Depends(get_rbac_service)


    @Controller.get('/', response_model=Page[RoleRead], dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def list_roles(self, pagination_params: Params = Depends()):
        return await self.service.list_roles(pagination_params)
    
    @Controller.post('/', response_model=RoleRead, dependencies=[Depends(HasPermission(PermissionAction.CREATE))])
    async def create_role(self, role: RoleCreate):
        return await self.service.create_role(role)
    
    @Controller.get('/{role_id}', response_model=RoleRead, dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def get_role(self, role_id: int):
        return await self.service.get_role(role_id)
    
    @Controller.patch('/{role_id}', response_model=RoleRead, dependencies=[Depends(HasPermission(PermissionAction.UPDATE))])
    async def patch_role(self, role_id: int, role: RoleUpdate):
        return await self.service.patch_role(role_id, role)
    
    @Controller.delete('/{role_id}', dependencies=[Depends(HasPermission(PermissionAction.DELETE))])
    async def delete_role(self, role_id: int):
        await self.service.delete_role(role_id)


class PermissionController(Controller):
    prefix = "/permissions"
    resource = "permissions"
    tags = ["Permissions", "RBAC"]

    service: RBACService = Depends(get_rbac_service)

    @Controller.get('/', response_model=Page[PermissionRead], dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def list_permissions(self, pagination_params: Params = Depends()):
        return await self.service.list_permissions(pagination_params)
    
    @Controller.post('/', response_model=PermissionRead, dependencies=[Depends(HasPermission(PermissionAction.CREATE))])
    async def create_permission(self, permission: PermissionCreate):
        return await self.service.create_permission(permission)
    
    @Controller.get('/{permission_id}', response_model=PermissionRead, dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def get_permission(self, permission_id: int):
        return await self.service.get_permission(permission_id)
    
    @Controller.patch('/{permission_id}', response_model=PermissionRead, dependencies=[Depends(HasPermission(PermissionAction.UPDATE))])
    async def patch_permission(self, permission_id: int, permission: PermissionUpdate):
        return await self.service.patch_permission(permission_id, permission)
    
    @Controller.delete('/{permission_id}', dependencies=[Depends(HasPermission(PermissionAction.DELETE))])
    async def delete_permission(self, permission_id: int):
        await self.service.delete_permission(permission_id)

        
