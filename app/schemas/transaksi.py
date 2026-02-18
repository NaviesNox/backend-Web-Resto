from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.pesanan import PesananResponse


class TransaksiBase(BaseModel):
    pesanan_id: int
    total_harga: float
    pajak: float = 0
    diskon: float = 0
    total_bayar: float


class TransaksiCreate(TransaksiBase):
    pass


class TransaksiUpdate(BaseModel):
    pajak: Optional[float] = None
    diskon: Optional[float] = None
    total_bayar: Optional[float] = None


class TransaksiResponse(TransaksiBase):
    id: int
    created_at: datetime
    updated_at: datetime
    pesanan: Optional[PesananResponse] = None

    class Config:
        from_attributes = True
