import uuid
from backend.models.users import Patient
from backend.repositories.patients import IPatientRepository, get_patient_repository
from backend.core.exceptions import MedServiceException, status
from backend.schemas import PatientUpdate
from backend.services.base import CRUDService
from fastapi import Depends


class PatientService(CRUDService[Patient, uuid.UUID]):
    def __init__(self, repo: IPatientRepository):
        super().__init__(repo)
        self.repo = repo


    async def patch(
        self, patient_id: uuid.UUID, patient: PatientUpdate
    ) -> Patient:
        instance = await self.get_by_id(patient_id)
        dump = patient.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
        if email := dump.get("email", None):
            if await self.repo.get_by_email(email) is not None:
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Email already exists",
                    f"Patient with email {email} already exists",
                )
        if phone_number := dump.get("phone_number", None):
            if await self.repo.get_by_phone_number(phone_number) is not None:
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Phone number already exists",
                    f"Patient with phone number {phone_number} already exists",
                )

        instance = await self.repo.update(instance, dump)
        return instance

def get_patient_service(repo: IPatientRepository = Depends(get_patient_repository)):
    return PatientService(repo)
