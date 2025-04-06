"""init

Revision ID: 3b6dc1af52a9
Revises: 
Create Date: 2025-03-31 11:50:44.920299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b6dc1af52a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('department_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_phone', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('department_id')
    )
    op.create_index(op.f('ix_departments_name'), 'departments', ['name'], unique=True)
    op.create_table('patients',
    sa.Column('patient_id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('birth_data', sa.Date(), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('patient_id')
    )
    op.create_index(op.f('ix_patients_email'), 'patients', ['email'], unique=True)
    op.create_index(op.f('ix_patients_phone_number'), 'patients', ['phone_number'], unique=True)
    op.create_table('permissions',
    sa.Column('permission_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('resource', sa.String(length=100), nullable=False),
    sa.Column('action', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('permission_id'),
    sa.UniqueConstraint('resource', 'action', name='uq_resource_action')
    )
    op.create_table('roles',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('doctors',
    sa.Column('doctor_id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.Column('specialization', sa.String(length=100), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('birth_data', sa.Date(), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], ),
    sa.PrimaryKeyConstraint('doctor_id')
    )
    op.create_index(op.f('ix_doctors_email'), 'doctors', ['email'], unique=True)
    op.create_index(op.f('ix_doctors_phone_number'), 'doctors', ['phone_number'], unique=True)
    op.create_table('role_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.permission_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('medical_records',
    sa.Column('record_id', sa.UUID(), nullable=False),
    sa.Column('patient_id', sa.UUID(), nullable=False),
    sa.Column('doctor_id', sa.UUID(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('examination_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.doctor_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.patient_id'], ),
    sa.PrimaryKeyConstraint('record_id')
    )
    op.create_table('medical_record_transcriptions',
    sa.Column('transcription_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('record_id', sa.UUID(), nullable=False),
    sa.Column('audio_url', sa.Text(), nullable=False),
    sa.Column('audio_duration', sa.Integer(), nullable=False),
    sa.Column('transcription_text', sa.Text(), nullable=False),
    sa.Column('asr_model', sa.String(length=100), nullable=False),
    sa.Column('asr_config', sa.JSON(), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=False),
    sa.ForeignKeyConstraint(['record_id'], ['medical_records.record_id'], ),
    sa.PrimaryKeyConstraint('transcription_id', 'record_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medical_record_transcriptions')
    op.drop_table('medical_records')
    op.drop_table('role_permissions')
    op.drop_index(op.f('ix_doctors_phone_number'), table_name='doctors')
    op.drop_index(op.f('ix_doctors_email'), table_name='doctors')
    op.drop_table('doctors')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_patients_phone_number'), table_name='patients')
    op.drop_index(op.f('ix_patients_email'), table_name='patients')
    op.drop_table('patients')
    op.drop_index(op.f('ix_departments_name'), table_name='departments')
    op.drop_table('departments')
    # ### end Alembic commands ###
