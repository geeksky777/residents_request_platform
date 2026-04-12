from aiokafka import AIOKafkaConsumer
import json
import asyncio
from app.config import settings
from app.database import async_session_factory


_consumer: AIOKafkaConsumer | None = None
_consumer_task: asyncio.Task | None = None

async def start_consumer():
    global _consumer, _consumer_task
    _consumer = AIOKafkaConsumer(
        "requests.created",                                  # топик, который слушаем
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="management-group",                         # группа консьюмеров, которые слушают этот топик
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset="earliest",                        # сбрасываем на начало топика, если нет смещения(offset)
    )
    await _consumer.start()
    _consumer_task = asyncio.create_task(_consume_loop())

async def stop_consumer():
    if _consumer_task:
        _consumer_task.cancel()
    if _consumer:
        await _consumer.stop()

async def _consume_loop():
    from app.service import handle_new_request
    async for message in _consumer:
        async with async_session_factory() as session:
            await handle_new_request(message.value, session)
            await session.commit()