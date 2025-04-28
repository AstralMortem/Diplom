from .users import PatientRead, PatientCreate, PatientDetailRead, PatientUpdate, DoctorCreate, DoctorRead, DoctorDetailRead, DoctorUpdate
from .auth import Gender, LoginResponse
from .departments import DepartmentCreate, DepartmentRead, DepartmentUpdate
from .records import MedRecordCreate, MedRecordRead, MedRecordUpdate, MedRecordDetailRead
from .rbac import RoleCreate, RoleRead, RoleUpdate, PermissionAction, PermissionRead, PermissionCreate, PermissionUpdate

__all__ = [
    "PatientRead", "PatientCreate", "PatientDetailRead", "PatientUpdate",
    "DoctorCreate", "DoctorRead", "DoctorDetailRead", "DoctorUpdate",
    "Gender", "LoginResponse",
    "DepartmentCreate", "DepartmentRead", "DepartmentUpdate",
    "MedRecordCreate", "MedRecordRead", "MedRecordUpdate",
    "RoleCreate", "RoleRead", "RoleUpdate",
    "PermissionAction", "PermissionRead", "PermissionCreate", "PermissionUpdate", "MedRecordDetailRead"
]
