import uuid
from backend.schemas import DoctorCreate, DoctorDetailRead, DoctorRead, DoctorUpdate
from backend.schemas.rbac import PermissionAction
from backend.utils.cbv import Controller
from backend.core.exceptions import status
from backend.services.doctors import get_doctor_service, DoctorService
from fastapi import Depends
from fastapi_pagination import Page, Params

from backend.utils.permission_helper import HasPermission


class DoctorController(Controller):
    prefix = "/doctors"
    resource = "doctors"
    tags = ["Doctors"]

    service: DoctorService = Depends(get_doctor_service)

    @Controller.get("/{doctor_id}", response_model=DoctorDetailRead, dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def get_doctor(self, doctor_id: uuid.UUID):
        return await self.service.get_by_id(doctor_id)

    @Controller.post("/", response_model=DoctorDetailRead, dependencies=[Depends(HasPermission(PermissionAction.CREATE))])
    async def create_doctor(self, doctor: DoctorCreate):
        return await self.service.create(doctor)

    @Controller.patch("/{doctor_id}", response_model=DoctorDetailRead, dependencies=[Depends(HasPermission(PermissionAction.UPDATE))])
    async def update_doctor(self, doctor_id: uuid.UUID, doctor: DoctorUpdate):
        return await self.service.patch(doctor_id, doctor)

    @Controller.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(HasPermission(PermissionAction.DELETE))])
    async def delete_doctor(self, doctor_id: uuid.UUID):
        await self.service.delete(doctor_id)

    @Controller.get("/", response_model=Page[DoctorRead], dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def list_doctors(self, pagination: Params = Depends()):
        return await self.service.list(pagination)
