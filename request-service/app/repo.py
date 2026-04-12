from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RequestCreate
from app.models import Request
from sqlalchemy import select
from uuid import UUID


async def create_request(request: RequestCreate, db: AsyncSession) -> Request:
    new_request = Request(
        title=request.title,
        description=request.description,
        resident_id=request.resident_id,
        building_id=request.building_id,
    )
    db.add(new_request)
    await db.flush()
    await db.refresh(new_request)
    return new_request


# async def get_all_requests(db: AsyncSession) -> list[Request]:
#     requests = await db.execute(select(Request))
#     return requests.scalars().all()


async def get_requests_by_resident_id(resident_id: int, db: AsyncSession) -> list[Request]:
    requests = await db.execute(select(Request).where(Request.resident_id == resident_id))
    return requests.scalars().all()



async def get_request_by_id(id: UUID, db: AsyncSession) -> Request:
    request = await db.execute(select(Request).where(Request.id == id))
    return request.scalar_one_or_none()