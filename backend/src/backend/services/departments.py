from backend.models.users import Department
from backend.repositories.departments import DepartmentRepository, get_department_repository
from fastapi import Depends
from .base import CRUDService


class DepartmentService(CRUDService[Department, int]):
    pass



async def get_department_service(repository: DepartmentRepository = Depends(get_department_repository)) -> DepartmentService:
    return DepartmentService(repository)
