from fastapi import HTTPException, status
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RequestCreate
from app.models import Request
from app.repo import create_request, get_request_by_id
from app.repo import get_all_requests
from app.repo import get_requests_by_resident_id


async def create_request_service(request: RequestCreate, db: AsyncSession) -> Request:
    new_request = await create_request(request, db)
    if not new_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create request")
    return new_request



async def get_all_requests_service(db: AsyncSession) -> list[Request]:
    requests = await get_all_requests(db)
    return requests



async def get_requests_by_resident_id_service(resident_id: int, db: AsyncSession) -> list[Request]:
    requests = await get_requests_by_resident_id(resident_id, db)
    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No requests found")
    return requests


async def get_request_by_id_service(id: UUID, db: AsyncSession) -> Request:
    request = await get_request_by_id(id, db)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No request found")
    return request