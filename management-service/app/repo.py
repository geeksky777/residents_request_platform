from uuid import UUID

from fastapi import HTTPException
from app.models import Request
from app.schemas import RequestUpdate
from app.database import StatusEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_requests(db: AsyncSession) -> list[Request]:
    requests  = await db.execute(select(Request))
    return requests.scalars().all()



async def update_request(request_id: UUID, request_to_update: RequestUpdate, db: AsyncSession) -> Request:
    request = await db.execute(select(Request).where(Request.id == request_id))
    request = request.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    new_request_data = request_to_update.model_dump(exclude_unset=True)
    for key, value in new_request_data.items():
        if hasattr(request, key):
            setattr(request, key, value)
    db.add(request)
    await db.flush()
    await db.refresh(request)
    return request


async def create_request(data: dict, db: AsyncSession) -> Request:
    request = Request(
        id=UUID(data["id"]),
        building_id=data["building_id"],
        title=data["title"],
        description=data["description"],
        status=StatusEnum(data["status"]),
    )
    db.add(request)
    await db.flush()
    await db.refresh(request)
    return request