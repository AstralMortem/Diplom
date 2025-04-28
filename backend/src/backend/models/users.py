from backend.core.db import Model
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Date, Enum, ForeignKey, String, Text, Boolean, Integer, UniqueConstraint
from backend.schemas.auth import Gender
from backend.schemas.rbac import PermissionAction
from datetime import date
import uuid

if TYPE_CHECKING:
    from backend.models.med_records import MedicalRecord


class PersonMixin:
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    birth_data: Mapped[date] = mapped_column(Date)
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class RolePermission(Model):
    __tablename__ = "role_permissions"
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True
    )


class Role(Model):
    __tablename__ = "roles"
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=RolePermission.__table__, lazy="joined"
    )


class Permission(Model):
    __tablename__ = "permissions"
    permission_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    resource: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(
        String(50), default=PermissionAction.RETRIEVE
    )

    __table_args__ = (UniqueConstraint("resource", "action", name="uq_resource_action"),)


class Department(Model):
    __tablename__ = "departments"
    department_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text())
    contact_phone: Mapped[str | None] = mapped_column(String(15))

    doctors: Mapped[list["Doctor"]] = relationship(lazy="joined", back_populates="department")


class Doctor(PersonMixin, Model):
    __tablename__ = "doctors"

    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(Text())
    specialization: Mapped[str] = mapped_column(String(100))
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.department_id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"))

    department: Mapped[Department | None] = relationship(lazy="selectin", back_populates="doctors")
    role: Mapped[Role] = relationship(lazy="joined")
    medical_records: Mapped[list["MedicalRecord"]] = relationship(lazy="joined", back_populates="doctor", viewonly=True)
    patients: Mapped[list["Patient"]] = relationship(lazy="joined", secondary="medical_records")


class Patient(PersonMixin, Model):
    __tablename__ = "patients"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str | None] = mapped_column(
        String(150), unique=True, index=True, nullable=True
    )
    address: Mapped[str] = mapped_column(Text())

    medical_records: Mapped[list["MedicalRecord"]] = relationship(lazy="joined", back_populates="patient", viewonly=True)
