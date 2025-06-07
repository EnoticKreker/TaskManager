from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )

class StartedAtMixin:
    started_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
class FinishAtMixin:
    finished_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

class StartAndFinishMixin(StartedAtMixin, FinishAtMixin):
    pass


class TimestampsMixin(CreatedAtMixin, StartAndFinishMixin):
    pass