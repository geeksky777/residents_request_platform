from pydantic import BaseModel
from app.database import StatusEnum
from pydantic import Field



class RequestUpdate(BaseModel):
    status: StatusEnum
    assigned_worker: int | None
    comments: str | None
