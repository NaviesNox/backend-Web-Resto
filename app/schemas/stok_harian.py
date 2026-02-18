from pydantic import BaseModel
from typing import Optional
from datetime import date


class StokHarianBase(BaseModel):
    menu_id: int
    tanggal: date
    stok_tersedia: int
    stok_terjual: int = 0


class StokHarianCreate(StokHarianBase):
    pass


class StokHarianUpdate(BaseModel):
    stok_tersedia: Optional[int] = None
    stok_terjual: Optional[int] = None


class StokHarianResponse(StokHarianBase):
    id: int

    class Config:
        from_attributes = True
