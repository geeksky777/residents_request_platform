from fastapi import APIRouter
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_db
from app.schemas import RequestCreate, RequestResponse
from app.service import create_request_service, get_request_by_id_service, get_requests_by_resident_id_service
from app.service import get_all_requests_service


router = APIRouter(prefix="/requests", tags=["requests"])



@router.post("/", response_model=RequestResponse)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    return await create_request_service(request, db)



@router.get("/", response_model=list[RequestResponse])
async def get_all_requests(db: AsyncSession = Depends(get_db)):
    return await get_all_requests_service(db)


@router.get("/resident", response_model=list[RequestResponse])
async def get_requests_by_resident_id(resident_id: int, db: AsyncSession = Depends(get_db)):
    return await get_requests_by_resident_id_service(resident_id, db)


@router.get("/{id}", response_model=RequestResponse)
async def get_request_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_request_by_id_service(id, db)