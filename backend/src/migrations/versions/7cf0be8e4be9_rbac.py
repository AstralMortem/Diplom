"""RBAC

Revision ID: 7cf0be8e4be9
Revises: ae8d6449574b
Create Date: 2025-05-27 17:12:56.900424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from backend.models.users import Role, Permission
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision: str = '7cf0be8e4be9'
down_revision: Union[str, None] = 'ae8d6449574b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def insert_permissions_to_role(role: Role, permissions: list[Permission]):
    for p in permissions:
        role.permissions.append(p)
    return role

def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    admin_role = Role(name="ADMIN") #ID: 1
    department_head_role = Role(name="DEPARTMENT_HEAD") #ID: 2
    doctor_role = Role(name="DOCTOR") #ID: 3
    intern_role = Role(name="INTERN") #ID: 4

    p1  = Permission(resource = "doctors", action = "create")
    p2  = Permission(resource = "doctors", action = "retrieve")
    p3  = Permission(resource = "doctors", action = "update")
    p4  = Permission(resource = "doctors", action = "delete")
    p5  = Permission(resource = "patients", action = "create")
    p6  = Permission(resource = "patients", action = "retrieve")
    p7  = Permission(resource = "patients", action = "update")
    p8  = Permission(resource = "patients", action = "delete")
    p9  = Permission(resource = "departments", action = "create")
    p10 = Permission(resource = "departments", action = "retrieve")
    p11 = Permission(resource =  "departments", action = "update")
    p12 = Permission(resource =  "departments", action = "delete")
    p13 = Permission(resource =  "medical_records", action = "create")
    p14 = Permission(resource =  "medical_records", action = "retrieve")
    p15 = Permission(resource =  "medical_records", action = "update")
    p16 = Permission(resource =  "medical_records", action = "delete")
    p17 = Permission(resource =  "transcriptions", action = "create")
    p18 = Permission(resource =  "transcriptions", action = "retrieve")
    p19 = Permission(resource =  "transcriptions", action = "delete")
    p20 = Permission(resource =  "files", action = "upload")
    p21 = Permission(resource =  "files", action = "delete")
    p22 = Permission(resource =  "roles", action = "create")
    p23 = Permission(resource =  "roles", action = "retrieve")
    p24 = Permission(resource =  "roles", action = "update")
    p25 = Permission(resource =  "roles", action = "delete")
    p26 = Permission(resource =  "permissions", action = "create")
    p27 = Permission(resource =  "permissions", action = "retrieve")
    p28 = Permission(resource =  "permissions", action = "update")
    p29 = Permission(resource =  "permissions", action = "delete")

    permissions = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29]

    session.add_all(permissions)

    admin_role = insert_permissions_to_role(admin_role, permissions)
    department_head_role = insert_permissions_to_role(department_head_role, [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20])
    doctor_role = insert_permissions_to_role( doctor_role, [p2,p3,p5,p6,p7,p8,p10,p13,p14,p15,p16,p17,p18,p19,p20])
    intern_role = insert_permissions_to_role(intern_role, [p2,p5,p6,p7,p8,p9,p10,p14,p17,p18,p20])
    
    session.add_all([admin_role, department_head_role, doctor_role, intern_role])
    session.commit()

def downgrade() -> None:
    op.execute("DELETE FROM permissions WHERE true")
    op.execute("DELETE FROM roles WHERE true")
