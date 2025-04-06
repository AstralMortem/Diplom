from backend.schemas.departments import DepartmentCreate, DepartmentRead, DepartmentUpdate
from backend.schemas.users import DepartmentDetailRead
from backend.services.departments import DepartmentService, get_department_service
from backend.utils.cbv import Controller
from fastapi import Depends
from fastapi_pagination import Page, Params


class DepartmentController(Controller):
    prefix = "/departments"
    resource = "departments"
    tags = ["Departments"]

    service: DepartmentService = Depends(get_department_service)

    @Controller.get('/', response_model=Page[DepartmentRead])
    async def list_departments(self, params: Params = Depends()):
        return await self.service.list(params)
    
    @Controller.get('/{department_id}', response_model=DepartmentDetailRead)
    async def get_department(self, department_id: int):
        return await self.service.get_by_id(department_id)
    
    @Controller.post('/', response_model=DepartmentRead)
    async def create_department(self, department: DepartmentCreate):
        return await self.service.create(department)
    
    @Controller.patch('/{department_id}', response_model=DepartmentRead )
    async def patch_department(self, department_id: int, department: DepartmentUpdate):
        return await self.service.patch(department_id, department)
    
    @Controller.delete('/{department_id}')
    async def delete_department(self, department_id: int):
        return await self.service.delete(department_id)
    

