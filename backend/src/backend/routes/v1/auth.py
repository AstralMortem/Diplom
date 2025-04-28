from backend.models.users import Doctor
from backend.schemas.auth import LoginResponse
from backend.schemas.users import DoctorDetailRead, DoctorUpdate
from backend.services.auth import authenticate, get_auth_service, AuthService

# from backend.utils.cbv_helper import Controller
from backend.utils.cbv import Controller
from fastapi import Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm


def test():
    return "test"


class AuthController(Controller):
    prefix = "/auth"
    resource = "auth"
    tags = ["auth"]

    service: AuthService = Depends(get_auth_service)

    @Controller.post(path="/login", response_model=LoginResponse)
    async def login(self, credentials: OAuth2PasswordRequestForm = Depends()):
        return await self.service.login(credentials.username, credentials.password)
    
    @Controller.post(path='/logout', status_code=status.HTTP_204_NO_CONTENT)
    async def logout(self, doctor: Doctor = Depends(authenticate)):
        return await self.service.logout()
    

    @Controller.post(path='/forgot-password')
    async def forgot_password(self, username: str = Body()):
        return None

    @Controller.get(path="/me", response_model=DoctorDetailRead)
    async def me(self, doctor: Doctor = Depends(authenticate)):
        return doctor

    @Controller.patch(path="/me", response_model=DoctorDetailRead)
    async def update_me(
        self, payload: DoctorUpdate, doctor: Doctor = Depends(authenticate)
    ):
        return await self.service.update_me(doctor, payload)
