from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import requests
from app.kafka.consumer import start_consumer, stop_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_consumer()     # запускаем консьюмер
    yield
    await stop_consumer()      # выключаем консьюмер
    # await engine.dispose()

app = FastAPI(lifespan=lifespan)


app.include_router(requests.router)


@app.get("/")
async def health_check():
    return {"status": "ok"}