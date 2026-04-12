from aiokafka import AIOKafkaProducer
import json
from app.config import settings
from app.models import Request



_producer: AIOKafkaProducer | None = None


async def start_producer():
    global _producer
    _producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: str(k).encode('utf-8'),
    )
    await _producer.start()



async def stop_producer():
    if _producer:
        await _producer.stop()


async def publish_request(request: Request) -> None:
    await _producer.send(
       topic="requests.created",
       key=request.building_id,
       value={
            "id": str(request.id),
            "title": request.title,
            "description": request.description,
            "resident_id": request.resident_id,
            "building_id": request.building_id,
            "status": request.status.value,
            "created_at": request.created_at.isoformat(),
       },
    )
