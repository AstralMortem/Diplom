"""Default RBAC

Revision ID: a54476c6ac1e
Revises: eb17085fbdf5
Create Date: 2025-04-08 13:01:41.081670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from backend.models.users import Role,  Permission

# revision identifiers, used by Alembic.
revision: str = 'a54476c6ac1e'
down_revision: Union[str, None] = 'eb17085fbdf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def insert_permission_to_role(role, permissions_list: list, exclude: list[int] = []) -> list[dict]:
    for permission in permissions_list:
        if not permission.permission_id in exclude:
            role.permissions.append(permission)
    return role


def upgrade() -> None:
    
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    
    admin_role = Role(role_id=1, name="admin")
    department_head_role = Role(role_id=2, name="department_head")
    doctor_role = Role(role_id=3, name="doctor")
    intern_role = Role(role_id=4, name="intern")
    session.add(admin_role)
    session.add(department_head_role)
    session.add(doctor_role)
    session.add(intern_role)

    permissions = [
        # Doctors
        {"permission_id": 1, "resource": "doctors", "action": "create"},
        {"permission_id": 2, "resource": "doctors", "action": "retrieve"},
        {"permission_id": 3, "resource": "doctors", "action": "update"},
        {"permission_id": 4, "resource": "doctors", "action": "delete"},

        # Patients
        {"permission_id": 5, "resource": "patients", "action": "create"},
        {"permission_id": 6, "resource": "patients", "action": "retrieve"},
        {"permission_id": 7, "resource": "patients", "action": "update"},
        {"permission_id": 8, "resource": "patients", "action": "delete"},
        
        # Departments
        {"permission_id": 9, "resource": "departments", "action": "create"},
        {"permission_id": 10, "resource": "departments", "action": "retrieve"},
        {"permission_id": 11, "resource": "departments", "action": "update"},
        {"permission_id": 12, "resource": "departments", "action": "delete"},
        
        # Medical Records
        {"permission_id": 13, "resource": "medical_records", "action": "create"},
        {"permission_id": 14, "resource": "medical_records", "action": "retrieve"},
        {"permission_id": 15, "resource": "medical_records", "action": "update"},
        {"permission_id": 16, "resource": "medical_records", "action": "delete"},
        
        # Transcriptions
        {"permission_id": 17, "resource": "transcriptions", "action": "create"},
        {"permission_id": 18, "resource": "transcriptions", "action": "retrieve"},
        {"permission_id": 19, "resource": "transcriptions", "action": "delete"},
        
        # Files

        {"permission_id": 20, "resource": "files", "action": "upload"},
        {"permission_id": 21, "resource": "files", "action": "delete"},
        
        # Roles
        {"permission_id": 22, "resource": "roles", "action": "create"},
        {"permission_id": 23, "resource": "roles", "action": "retrieve"},
        {"permission_id": 24, "resource": "roles", "action": "update"},
        {"permission_id": 25, "resource": "roles", "action": "delete"},
        
        # Permissions

        {"permission_id": 26, "resource": "permissions", "action": "create"},
        {"permission_id": 27, "resource": "permissions", "action": "retrieve"},
        {"permission_id": 28, "resource": "permissions", "action": "update"},
        {"permission_id": 29, "resource": "permissions", "action": "delete"},    
    ]

    permission_objects = []
    
    for permission in permissions:
        permission_objects.append(Permission(**permission))

    session.add_all(permission_objects)

    admin_role = insert_permission_to_role(admin_role, permission_objects)
    department_head_role = insert_permission_to_role(department_head_role, permission_objects, [21,22,23,24,25,26,27,28,29])
    doctor_role = insert_permission_to_role(doctor_role, permission_objects, [1,4,9,11,12,21,22,23,24,25,26,27,28,29])
    intern_role = insert_permission_to_role(intern_role, permission_objects, [1,3,4,7,8,9,11,12,13,15,16,19,21,22,23,24,25,26,27,28,29])

    session.commit()
    

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM permissions WHERE true")
    op.execute("DELETE FROM roles WHERE true")

