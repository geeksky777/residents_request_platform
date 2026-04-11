from uuid import uuid4
from sqlalchemy import UUID, DateTime, Integer, String, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.database import StatusEnum
from datetime import datetime


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    resident_id: Mapped[int] = mapped_column(Integer,nullable=False)
    building_id: Mapped[int] = mapped_column(Integer,nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum"),
        nullable=False,
        default=StatusEnum.PENDING,
        server_default=StatusEnum.PENDING.value,
    )
    assigned_worker: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
