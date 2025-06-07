from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from crud.tasks import create_task as crud_create_task, crud_delete_task, get_task, get_tasks
from schemas.tasks import TaskCreate, Task as TaskSchema, TaskStatusResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from core.rabmq_producer import send_task_message


router = APIRouter()

class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

class DatabaseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {detail}"
        )
        

@router.post("/tasks/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        created_task = await crud_create_task(db, task)
        
        print(created_task)
        
        await send_task_message({
            "id": str(created_task.id),
            "title": created_task.title,
            "description": created_task.description,
            "status": created_task.status,
            "result": created_task.result,
            "error": created_task.error,
        })
        
        return created_task
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error. {e}'
        )

@router.delete("/tasks/{task_id}", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        task = await crud_delete_task(db, task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error. {e}'
        )

@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def read_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        task = await get_task(db, task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error. {e}'
        )

@router.get("/tasks/", response_model=List[TaskSchema])
async def all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    try:
        tasks = await get_tasks(db, skip=skip, limit=limit)
        return tasks
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error. {e}'
        )


@router.get("/tasks/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        task = await get_task(db, task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return {"status": task.status}
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal server error. {e}'
        )
        