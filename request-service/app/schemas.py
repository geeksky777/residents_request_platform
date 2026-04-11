from pydantic import BaseModel, Field
from app.database import StatusEnum
from datetime import datetime
from uuid import UUID
from pydantic import ConfigDict


class RequestCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    resident_id: int = Field(..., ge=1)
    building_id: int = Field(..., ge=1)



class RequestResponse(BaseModel):
    id: UUID
    title: str
    description: str
    resident_id: int
    building_id: int
    status: StatusEnum
    assigned_worker: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

