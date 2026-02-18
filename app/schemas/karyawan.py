from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KaryawanBase(BaseModel):
    nama: str
    alamat: Optional[str] = None
    no_telepon: Optional[str] = None
    posisi: str
    user_id: Optional[int] = None


class KaryawanCreate(KaryawanBase):
    pass


class KaryawanUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    no_telepon: Optional[str] = None
    posisi: Optional[str] = None
    user_id: Optional[int] = None


class KaryawanResponse(KaryawanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
