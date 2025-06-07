from typing import Optional
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

class TaskOptionalFields:
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)