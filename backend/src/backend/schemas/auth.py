from enum import StrEnum
from backend.schemas.base import Schema


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"



class LoginResponse(Schema):
    access_token: str
    token_type: str = 'bearer'