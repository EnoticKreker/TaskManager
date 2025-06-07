from enum import Enum
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

class TaskStatus(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    
class TaskOptionalFields(BaseModel):
    result: Optional[str] = None
    error: Optional[str] = None
    
class TaskStatusResponse(BaseModel):
    status: TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskCreate(TaskBase, TaskOptionalFields):
    status: Optional[TaskStatus] = Field(default=TaskStatus.NEW)

class TaskUpdate(TaskCreate):
    pass

class Task(TaskBase, TaskOptionalFields):
    id: UUID
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = SettingsConfigDict(from_attributes=True)