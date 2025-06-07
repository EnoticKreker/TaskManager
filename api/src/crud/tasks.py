from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from schemas.tasks import TaskCreate, TaskUpdate
from db.models.task import Task
from uuid import UUID

async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        print("Ошибка при коммите:", e)
        raise
    await db.refresh(db_task)
    return db_task

async def get_task(db: AsyncSession, task_id: UUID):
    result = await db.execute(select(Task).where( Task.id == task_id))
    return result.scalars().first()

async def crud_delete_task(db: AsyncSession, task_id: UUID):
    result = await db.execute(
        delete(Task)
        .where(Task.id == task_id)
        .returning(Task)
    )
    task = result.scalar_one_or_none()
    await db.commit()
    return task

async def update_task(db: AsyncSession, task_id: UUID, task_update:  TaskUpdate):
    stmt = (
        update( Task)
        .where( Task.id == task_id)
        .values(**task_update.model_dump(exclude_unset=True)))
    await db.execute(stmt)
    await db.commit()
    return await get_task(db, task_id)

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()