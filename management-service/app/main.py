from fastapi import FastAPI
from contextlib import asynccontextmanager


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     #startup(kafka)
#     yield
#     #shutdown(kafka)
#     # await engine.dispose()

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}