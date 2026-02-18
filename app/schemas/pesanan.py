from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.pesanan import StatusPesanan


# Simple nested schemas to avoid circular imports
class SimpleMenuResponse(BaseModel):
    id: int
    nama: str
    harga: float
    
    class Config:
        from_attributes = True


class SimpleMejaResponse(BaseModel):
    id: int
    nomor_meja: str
    kapasitas: int
    
    class Config:
        from_attributes = True


class SimpleKaryawanResponse(BaseModel):
    id: int
    nama: str
    
    class Config:
        from_attributes = True


class DetailPesananBase(BaseModel):
    menu_id: int
    jumlah: int
    harga_satuan: float
    subtotal: float
    catatan: Optional[str] = None


class DetailPesananCreate(DetailPesananBase):
    pass


class DetailPesananResponse(DetailPesananBase):
    id: int
    pesanan_id: int
    created_at: datetime
    menu: Optional[SimpleMenuResponse] = None

    class Config:
        from_attributes = True


class PesananBase(BaseModel):
    meja_id: int
    karyawan_id: int
    nama_pelanggan: Optional[str] = None
    status: StatusPesanan = StatusPesanan.PENDING


class PesananCreate(BaseModel):
    meja_id: int
    karyawan_id: int
    nama_pelanggan: Optional[str] = None
    items: List[DetailPesananCreate]


class PesananUpdate(BaseModel):
    status: Optional[StatusPesanan] = None


class PesananResponse(PesananBase):
    id: int
    created_at: datetime
    updated_at: datetime
    detail_pesanan: List[DetailPesananResponse] = []
    meja: Optional[SimpleMejaResponse] = None
    karyawan: Optional[SimpleKaryawanResponse] = None

    class Config:
        from_attributes = True
