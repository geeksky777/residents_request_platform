from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import requests



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     #startup(kafka)
#     yield
#     #shutdown(kafka)
#     # await engine.dispose()

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(requests.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}