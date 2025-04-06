import uuid
from backend.schemas import DoctorCreate, DoctorDetailRead, DoctorRead, DoctorUpdate
from backend.utils.cbv import Controller
from backend.core.exceptions import status
from backend.services.doctors import get_doctor_service, DoctorService
from fastapi import Depends
from fastapi_pagination import Page, Params


class DoctorController(Controller):
    prefix = "/doctors"
    resource = "doctors"
    tags = ["Doctors"]

    service: DoctorService = Depends(get_doctor_service)

    @Controller.get("/{doctor_id}", response_model=DoctorDetailRead)
    async def get_doctor(self, doctor_id: uuid.UUID):
        return await self.service.get_by_id(doctor_id)

    @Controller.post("/", response_model=DoctorDetailRead)
    async def create_doctor(self, doctor: DoctorCreate):
        return await self.service.create(doctor)

    @Controller.patch("/{doctor_id}", response_model=DoctorDetailRead)
    async def update_doctor(self, doctor_id: uuid.UUID, doctor: DoctorUpdate):
        return await self.service.patch(doctor_id, doctor)

    @Controller.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_doctor(self, doctor_id: uuid.UUID):
        await self.service.delete(doctor_id)

    @Controller.get("/", response_model=Page[DoctorRead])
    async def list_doctors(self, pagination: Params = Depends()):
        return await self.service.list(pagination)
