from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.meja import StatusMeja


class MejaBase(BaseModel):
    nomor_meja: str
    kapasitas: int
    status: StatusMeja = StatusMeja.TERSEDIA
    is_active: bool = True


class MejaCreate(MejaBase):
    pass


class MejaUpdate(BaseModel):
    nomor_meja: Optional[str] = None
    kapasitas: Optional[int] = None
    status: Optional[StatusMeja] = None
    is_active: Optional[bool] = None


class MejaResponse(MejaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
