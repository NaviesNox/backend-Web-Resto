from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.pembayaran import MetodePembayaran
from app.schemas.transaksi import TransaksiResponse


class PembayaranBase(BaseModel):
    transaksi_id: int
    metode_pembayaran: MetodePembayaran
    jumlah_bayar: float
    kembalian: float = 0


class PembayaranCreate(PembayaranBase):
    pass


class PembayaranResponse(PembayaranBase):
    id: int
    created_at: datetime
    transaksi: Optional[TransaksiResponse] = None

    class Config:
        from_attributes = True
