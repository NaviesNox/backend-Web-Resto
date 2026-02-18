from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KategoriMenuBase(BaseModel):
    nama: str
    deskripsi: Optional[str] = None
    is_active: bool = True


class KategoriMenuCreate(KategoriMenuBase):
    pass


class KategoriMenuUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None
    is_active: Optional[bool] = None


class KategoriMenuResponse(KategoriMenuBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
