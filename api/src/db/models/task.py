from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from db.mixins.optional_fields import TaskOptionalFields
from db.mixins.id_mixins import IDMixin
from db.mixins.timestamp_mixins import TimestampsMixin
from schemas.tasks import TaskPriority, TaskStatus
from core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Task(Base, IDMixin, TimestampsMixin, TaskOptionalFields):
    __tablename__ = "tasks"
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.NEW
    )