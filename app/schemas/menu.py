from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MenuBase(BaseModel):
    nama: str
    deskripsi: Optional[str] = None
    harga: float
    kategori_id: int
    gambar_url: Optional[str] = None
    is_available: bool = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None
    harga: Optional[float] = None
    kategori_id: Optional[int] = None
    gambar_url: Optional[str] = None
    is_available: Optional[bool] = None


class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
