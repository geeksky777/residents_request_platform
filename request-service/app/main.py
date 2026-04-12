from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import requests
from app.kafka.producer import start_producer, stop_producer



@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer()   # запускаем при старте приложения
    yield
    await stop_producer()    # выключаем при остановке
    # await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(requests.router)


@app.get("/")
async def health_check():
    return {"status": "ok"}