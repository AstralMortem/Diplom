from backend.schemas import PatientCreate, PatientDetailRead, PatientRead, PatientUpdate
from backend.schemas.rbac import PermissionAction
from backend.services.patients import PatientService, get_patient_service
from backend.utils.cbv import Controller
from fastapi import Depends, status
import uuid

from fastapi_pagination import Page, Params

from backend.utils.permission_helper import HasPermission


class PatientController(Controller):
    prefix = "/patients"
    resource = "patients"
    tags = ["patients"]

    service: PatientService = Depends(get_patient_service)

    @Controller.get("/{patient_id}", response_model=PatientDetailRead, dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def get_patient(self, patient_id: uuid.UUID):
        return await self.service.get_by_id(patient_id)

    @Controller.post("/", response_model=PatientDetailRead, dependencies=[Depends(HasPermission(PermissionAction.CREATE))])
    async def create_patient(self, patient: PatientCreate):
        return await self.service.create(patient)

    @Controller.patch("/{patient_id}", response_model=PatientDetailRead, dependencies=[Depends(HasPermission(PermissionAction.UPDATE))])
    async def patch_patient(self, patient_id: uuid.UUID, patient: PatientUpdate):
        return await self.service.patch(patient_id, patient)

    @Controller.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(HasPermission(PermissionAction.DELETE))])
    async def delete_patient(self, patient_id: uuid.UUID):
        await self.service.delete(patient_id)

    @Controller.get("/", response_model=Page[PatientRead], dependencies=[Depends(HasPermission(PermissionAction.RETRIEVE))])
    async def list_patients(self, pagination: Params = Depends()):
        return await self.service.list(pagination)

    
