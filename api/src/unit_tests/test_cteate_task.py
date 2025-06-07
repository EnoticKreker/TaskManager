from unittest.mock import AsyncMock, MagicMock
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from crud.tasks import create_task, crud_delete_task, get_task
from db.models.task import Task
from datetime import datetime, timezone
from schemas.tasks import TaskCreate, Task, TaskStatus, TaskPriority

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

@pytest.mark.asyncio
async def test_create_task(mocker):
    fake_db = mocker.Mock(spec=AsyncSession)
    fake_task_data = TaskCreate(title="Test", description="Testing", priority="LOW")
    
    mock_task = Task(
        id=uuid4(),
        title="Test",
        description="Testing",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        created_at=datetime.now(timezone.utc),
        started_at=None,
        finished_at=None,
        result=None,
        error=None
    )
    mocker.patch("db.models.task.Task", return_value=mock_task)
    fake_db.add.return_value = None
    fake_db.commit.return_value = None
    fake_db.refresh.return_value = None

    result = await create_task(fake_db, fake_task_data)

    assert result.title == "Test"
    
    
@pytest.mark.asyncio
async def test_crud_delete_task(mocker):
    fake_db = mocker.Mock(spec=AsyncSession)
    task_id = uuid4()

    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        created_at=datetime.now(timezone.utc),
        started_at=None,
        finished_at=None,
        result=None,
        error=None
    )
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task

    fake_db.execute = AsyncMock(return_value=mock_result)

    fake_db.commit = AsyncMock()

    result = await crud_delete_task(fake_db, task_id)

    called_args = fake_db.execute.call_args.args[0]
    assert str(called_args.compile(compile_kwargs={"literal_binds": True})).startswith("DELETE FROM")
    
    assert result == mock_task

    fake_db.commit.assert_awaited_once()
    

@pytest.mark.asyncio
async def test_get_status_task(mocker):
    fake_db = mocker.Mock(spec=AsyncSession)
    task_id = uuid4()

    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.COMPLETED,
        created_at=datetime.now(timezone.utc),
        started_at=None,
        finished_at=None,
        result=None,
        error=None
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_task
    fake_db.execute = AsyncMock(return_value=mock_result)
    fake_db.commit = AsyncMock()
    result = await get_task(fake_db, task_id)
    
    assert result.status == mock_task.status
    
    
    