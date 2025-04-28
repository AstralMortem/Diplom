from datetime import datetime, timedelta, UTC
from typing import Any
import uuid
from backend.models.users import Doctor
from backend.repositories.doctors import (
    IDoctorRepository,
    SQLDoctorRepository,
    get_doctor_repository,
)
from backend.core import MedServiceException, status
from backend.schemas.auth import LoginResponse
from backend.schemas.users import DoctorUpdate
from backend.utils.password_helper import PasswordHelper, PasswordHelperProtocol
from backend.config import config
from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
import jwt


class AuthService:
    def __init__(self, doctor_repository: IDoctorRepository):
        self.doctor_repository = doctor_repository
        self.password_helper: PasswordHelperProtocol = PasswordHelper()

    async def login(self, username: str, password: str):
        error = MedServiceException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
            "Invalid Email/Phone or Password",
        )

        doctor = await self.doctor_repository.get_doctor_for_login(username)
        if doctor is None:
            raise error

        is_valid, new_hash = self.password_helper.verify_and_update(
            password, doctor.hashed_password
        )
        if not is_valid:
            raise error

        if new_hash is not None:
            doctor = await self.doctor_repository.update(
                doctor, {"hashed_password": new_hash}
            )

        if not doctor.is_active:
            raise error

        return self._create_login_response(doctor)

    async def logout(self):
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(config.AUTH_COOKIE_NAME)
        return response

    async def update_me(
        self, instance: Doctor, payload: DoctorUpdate, safe: bool = True
    ) -> Doctor:
        dump = payload.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
        if safe:
            dump = payload.model_dump(
                exclude_none=True,
                exclude_defaults=True,
                exclude_unset=True,
                exclude={"role_id", "department_id"},
            )

        if password := dump.get("password", None):
            dump["hashed_password"] = self.password_helper.hash(password)

        if email := dump.get("email", None):
            if await self.doctor_repository.get_by_email(email) is not None:
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Email already exists",
                    "Email already exists",
                )

        if phone_number := dump.get("phone_number", None):
            if (
                await self.doctor_repository.get_by_phone_number(phone_number)
                is not None
            ):
                raise MedServiceException(
                    status.HTTP_400_BAD_REQUEST,
                    "Phone number already exists",
                    "Phone number already exists",
                )

        instance = await self.doctor_repository.update(instance, dump)
        return instance

    async def authenticate(self, token: str) -> Doctor:
        error = lambda e: MedServiceException(
            status.HTTP_401_UNAUTHORIZED, "Invalid token", "Invalid token", debug=e
        )
        decoded_token = self._decode_auth_token(token)

        try:
            doctor_id = decoded_token["sub"]
        except KeyError as e:
            raise error(e)

        try:
            doctor_id = uuid.UUID(doctor_id)
        except ValueError as e:
            raise error(e)

        doctor = await self.doctor_repository.get_by_id(doctor_id)
        if doctor is None:
            raise error(None)

        if not doctor.is_active:
            raise error(None)

        return doctor

    def _generate_auth_token(self, doctor: Doctor) -> str:
        payload = {
            "sub": str(doctor.doctor_id),
            "exp": datetime.now(UTC) + timedelta(seconds=config.JWT_EXPIRATION_TIME),
            "iat": datetime.now(UTC),
            "aud": config.JWT_AUTH_AUDIENCE,
        }
        return jwt.encode(
            payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
        )

    def _decode_auth_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
                audience=config.JWT_AUTH_AUDIENCE,
            )
        except jwt.PyJWTError as error:
            raise MedServiceException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid token",
                "Invalid token",
                debug=error,
            )

    def _create_login_response(self, doctor: Doctor) -> Response:
        token = self._generate_auth_token(doctor)
        response = JSONResponse(content=LoginResponse(access_token=token).model_dump())
        response.set_cookie(
            config.AUTH_COOKIE_NAME,
            token,
            max_age=config.JWT_EXPIRATION_TIME,
        )
        return response


async def get_auth_service(
    doctor_repository: SQLDoctorRepository = Depends(get_doctor_repository),
):
    return AuthService(doctor_repository)


# cookie_key = APIKeyCookie(name=config.AUTH_COOKIE_NAME, auto_error=False)
header_key = OAuth2PasswordBearer(config.LOGIN_URL, auto_error=False)


async def authenticate(
    service: AuthService = Depends(get_auth_service), token: str | None = Depends(header_key)
):
    if token is None:
        raise MedServiceException(
            status.HTTP_401_UNAUTHORIZED, "Unauthorized", "Auth Token not set"
        )
    return await service.authenticate(token)
