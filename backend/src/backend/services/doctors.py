import uuid

from backend.core.exceptions import MedServiceException, status
from backend.models.users import Doctor
from backend.repositories.doctors import IDoctorRepository, get_doctor_repository
from backend.schemas import DoctorCreate, DoctorUpdate
from backend.utils.password_helper import PasswordHelper, PasswordHelperProtocol
from fastapi import Depends
from .base import CRUDService
from backend.config import config

class DoctorService(CRUDService[Doctor, uuid.UUID]):

    def __init__(self, repository: IDoctorRepository):
        super().__init__(repository)
        self.repo = repository
        self.password_helper: PasswordHelperProtocol = PasswordHelper()


    async def create(self, doctor: DoctorCreate, safe: bool = True) -> Doctor:

        error = MedServiceException(status.HTTP_400_BAD_REQUEST, "Doctor already exists", "Doctor with email or phone number already exists")
        if await self.repo.get_by_email(doctor.email) is not None:
            raise error
        if await self.repo.get_by_phone_number(doctor.phone_number) is not None:
            raise error
        
        dump = doctor.model_dump(exclude_unset=True)
        if safe:
            dump["role_id"] = config.DEFAULT_DOCTOR_ROLE_ID

        dump["hashed_password"] = self.password_helper.hash(dump.pop("password"))
        
        instance = await self.repo.create(dump)
        return instance
        

    async def patch(
        self, id: uuid.UUID, doctor: DoctorUpdate
    ) -> Doctor:
        instance = await self.get_by_id(id)
        dump = doctor.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
        if email := dump.get("email", None):
            if await self.repo.get_by_email(email) is not None:
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Email already exists",
                    f"Doctor with email {email} already exists",
                )
        if phone_number := dump.get("phone_number", None):
            if await self.repo.get_by_phone_number(phone_number) is not None:
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Phone number already exists",
                    f"Doctor with phone number {phone_number} already exists",
                )

        if password := dump.get("password", None):
            dump["hashed_password"] = self.password_helper.hash(password)

        instance = await self.repo.update(instance, dump)
        return instance

async def get_doctor_service(
    repository: IDoctorRepository = Depends(get_doctor_repository),
) -> DoctorService:
    return DoctorService(repository)

