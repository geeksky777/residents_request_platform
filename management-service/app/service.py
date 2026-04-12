from uuid import UUID
from app.repo import get_requests
from app.models import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RequestUpdate
from app.repo import update_request
from app.repo import create_request



async def get_requests_service(db: AsyncSession) -> list[Request]:
    requests = await get_requests(db)
    return requests

async def update_request_service(request_id: UUID, request_to_update: RequestUpdate, db: AsyncSession) -> Request:
    request = await update_request(request_id, request_to_update, db)
    await db.commit()
    return request

async def handle_new_request(data: dict, db: AsyncSession) -> None:
    await create_request(data, db)