import json
import asyncio
import aio_pika
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq")

async def wait_for_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            await connection.close()
            break
        except Exception:
            print("[Consumer] Ожидание RabbitMQ...")
            await asyncio.sleep(2)

async def handle_message(message: aio_pika.IncomingMessage):
    print("[Consumer] handle_message вызван", flush=True)
    print("[Consumer] Получено сообщение", flush=True)
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            print(f"[Consumer] Получена задача: {data}", flush=True)
        except Exception as e:
            print(f"[Consumer] Ошибка при обработке сообщения: {e}", flush=True)


async def main():
    print("[Consumer] Запуск consumer...")

    print(f"[Consumer] Подключение к RabbitMQ: {RABBITMQ_URL}")
    await wait_for_rabbitmq()

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange("tasks", aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue("worker_queue", durable=True)
    await queue.bind(exchange)

    await queue.consume(handle_message)

    print("[Consumer] Ожидание сообщений...", flush=True)
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
