import aio_pika
import json
from fastapi import FastAPI

import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

connection = None
channel = None
exchange = None

async def init_rabbitmq():
    global connection, channel, exchange
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("tasks", aio_pika.ExchangeType.FANOUT)

async def send_task_message(task_data: dict):
    message = aio_pika.Message(body=json.dumps(task_data).encode())
    await exchange.publish(message, routing_key="")
    print("[Producer] Сообщение отправлено", flush=True)