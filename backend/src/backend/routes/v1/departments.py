from backend.schemas.departments import DepartmentCreate, DepartmentRead, DepartmentUpdate
from backend.schemas.rbac import PermissionAction
from backend.schemas.users import DepartmentDetailRead
from backend.services.departments import DepartmentService, get_department_service
from backend.utils.cbv import Controller
from fastapi import Depends
from fastapi_pagination import Page, Params

from backend.utils.permission_helper import HasPermission


class DepartmentController(Controller):
    prefix = "/departments"
    resource = "departments"
    tags = ["Departments"]

    service: DepartmentService = Depends(get_department_service)

    @Controller.get('/', response_model=Page[DepartmentRead], dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def list_departments(self, params: Params = Depends()):
        return await self.service.list(params)
    
    @Controller.get('/{department_id}', response_model=DepartmentDetailRead, dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def get_department(self, department_id: int):
        instance = await self.service.get_by_id(department_id)
        print(instance.doctors)
        return instance

    @Controller.post('/', response_model=DepartmentRead, dependencies=[Depends(HasPermission(PermissionAction.CREATE))])
    async def create_department(self, department: DepartmentCreate):
        return await self.service.create(department)
    
    @Controller.patch('/{department_id}', response_model=DepartmentRead, dependencies=[Depends(HasPermission(PermissionAction.UPDATE))] )
    async def patch_department(self, department_id: int, department: DepartmentUpdate):
        return await self.service.patch(department_id, department)
    
    @Controller.delete('/{department_id}', dependencies=[Depends(HasPermission(PermissionAction.DELETE))])
    async def delete_department(self, department_id: int):
        return await self.service.delete(department_id)
    

