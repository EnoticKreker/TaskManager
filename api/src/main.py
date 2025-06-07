from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from core.rabmq_producer import init_rabbitmq
from core.database import engine, Base
from router.api import router
from sqlalchemy.exc import SQLAlchemyError

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_rabbitmq()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router, prefix="/api/v1")