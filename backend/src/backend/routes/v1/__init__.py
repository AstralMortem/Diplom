from fastapi import APIRouter
from backend.config import config
from backend.routes.v1.auth import AuthController
from backend.routes.v1.patitents import PatientController
from backend.routes.v1.records import MedRecordController
from backend.routes.v1.doctors import DoctorController
from backend.routes.v1.rbac import RoleController, PermissionController
from backend.routes.v1.departments import DepartmentController
from backend.routes.v1.files import file_router


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(AuthController.as_router())
v1_router.include_router(PatientController.as_router())
v1_router.include_router(MedRecordController.as_router())
v1_router.include_router(DoctorController.as_router())
v1_router.include_router(RoleController.as_router())
v1_router.include_router(PermissionController.as_router())
v1_router.include_router(DepartmentController.as_router())
v1_router.include_router(file_router)
