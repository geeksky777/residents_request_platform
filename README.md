<!--
Only for myself
Instruction how to stand up docker 
docker compose up -d request-db management-db kafka kafka-ui
Kafka UI откроется на http://localhost:8080.
 -->

<!-- 7. No lifespan handler — Kafka consumers will never start


main.py
Lines 1-7
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def health_check():
    return {"status": "ok"}
aiokafka consumers run as long-lived async loops. Without a lifespan context manager, there is no place to start (await consumer.start()) or stop (await consumer.stop()) them. The architecture calls for request-service to consume requests.updated and management-service to consume requests.created, but as written, no consumer will ever run. Additionally, the SQLAlchemy engine pool is never explicitly disposed on shutdown. -->


<!-- 11. KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true" in production setup


docker-compose.yml
Lines 61-61
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
Auto-creation uses broker defaults for partition count (1), replication factor (1), and retention. Topics are implicitly created on first produce/consume — there is no guarantee the producer and consumer agree on topic names, partition layout, or retention policy. Topics should be explicitly pre-created with controlled configuration. -->