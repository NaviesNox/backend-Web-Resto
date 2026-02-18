from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.pembayaran import Pembayaran
from app.models.transaksi import Transaksi
from app.models.pesanan import Pesanan
from app.models.detail_pesanan import DetailPesanan
from app.models.user import User, UserRole
from app.schemas.pembayaran import PembayaranCreate, PembayaranResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/pembayaran", tags=["Pembayaran"])


def _pembayaran_options():
    return [
        joinedload(Pembayaran.transaksi).joinedload(Transaksi.pesanan).joinedload(Pesanan.meja),
        joinedload(Pembayaran.transaksi).joinedload(Transaksi.pesanan).joinedload(Pesanan.karyawan),
        joinedload(Pembayaran.transaksi).joinedload(Transaksi.pesanan).joinedload(Pesanan.detail_pesanan).joinedload(DetailPesanan.menu),
    ]


@router.get("/", response_model=List[PembayaranResponse])
async def get_pembayaran(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    pembayaran = db.query(Pembayaran).options(*_pembayaran_options()).offset(skip).limit(limit).all()
    return pembayaran


@router.get("/{pembayaran_id}", response_model=PembayaranResponse)
async def get_pembayaran_by_id(
    pembayaran_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    pembayaran = db.query(Pembayaran).options(*_pembayaran_options()).filter(Pembayaran.id == pembayaran_id).first()
    if not pembayaran:
        raise HTTPException(status_code=404, detail="Pembayaran not found")
    return pembayaran


@router.post("/", response_model=PembayaranResponse, status_code=status.HTTP_201_CREATED)
async def create_pembayaran(
    pembayaran: PembayaranCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    # Cek transaksi ada
    transaksi = db.query(Transaksi).filter(Transaksi.id == pembayaran.transaksi_id).first()
    if not transaksi:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    # Cek belum dibayar
    existing = db.query(Pembayaran).filter(Pembayaran.transaksi_id == pembayaran.transaksi_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Transaksi ini sudah dibayar")

    db_pembayaran = Pembayaran(**pembayaran.model_dump())
    db.add(db_pembayaran)
    db.commit()
    db.refresh(db_pembayaran)
    # Re-query with relationships loaded
    db_pembayaran = db.query(Pembayaran).options(*_pembayaran_options()).filter(Pembayaran.id == db_pembayaran.id).first()
    return db_pembayaran


@router.delete("/{pembayaran_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pembayaran(
    pembayaran_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_pembayaran = db.query(Pembayaran).filter(Pembayaran.id == pembayaran_id).first()
    if not db_pembayaran:
        raise HTTPException(status_code=404, detail="Pembayaran not found")
    
    db.delete(db_pembayaran)
    db.commit()
    return None
