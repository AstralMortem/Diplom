from enum import StrEnum
from backend.schemas.base import Schema


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class LoginCredentials(Schema):
    username: str
    password: str
