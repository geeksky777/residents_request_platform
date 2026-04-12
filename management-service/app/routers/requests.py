from uuid import UUID
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_db
from app.service import get_requests_service, update_request_service
from app.schemas import RequestUpdate


router = APIRouter(prefix="/management", tags=["management"])

@router.get("/requests")
async def get_requests(db: AsyncSession = Depends(get_db)):
    requests = await get_requests_service(db)
    return requests


@router.put("/requests/{request_id}")
async def update_request(request_id: UUID, request_to_update: RequestUpdate, db: AsyncSession = Depends(get_db)):
    request = await update_request_service(request_id, request_to_update, db)
    return request  

