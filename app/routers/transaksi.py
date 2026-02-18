from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.transaksi import Transaksi
from app.models.pesanan import Pesanan
from app.models.detail_pesanan import DetailPesanan
from app.models.menu import Menu
from app.models.meja import Meja
from app.models.karyawan import Karyawan
from app.models.user import User, UserRole
from app.schemas.transaksi import TransaksiCreate, TransaksiUpdate, TransaksiResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/transaksi", tags=["Transaksi"])


def _transaksi_options():
    return [
        joinedload(Transaksi.pesanan).joinedload(Pesanan.detail_pesanan).joinedload(DetailPesanan.menu),
        joinedload(Transaksi.pesanan).joinedload(Pesanan.meja),
        joinedload(Transaksi.pesanan).joinedload(Pesanan.karyawan),
    ]


@router.get("/", response_model=List[TransaksiResponse])
async def get_transaksi(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    transaksi = db.query(Transaksi).options(
        *_transaksi_options()
    ).offset(skip).limit(limit).all()
    return transaksi


@router.get("/{transaksi_id}", response_model=TransaksiResponse)
async def get_transaksi_by_id(
    transaksi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    transaksi = db.query(Transaksi).options(
        *_transaksi_options()
    ).filter(Transaksi.id == transaksi_id).first()
    if not transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    return transaksi


@router.post("/", response_model=TransaksiResponse, status_code=status.HTTP_201_CREATED)
async def create_transaksi(
    transaksi: TransaksiCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    db_transaksi = Transaksi(**transaksi.model_dump())
    db.add(db_transaksi)
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi


@router.put("/{transaksi_id}", response_model=TransaksiResponse)
async def update_transaksi(
    transaksi_id: int,
    transaksi: TransaksiUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.KASIR]))
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not db_transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    
    update_data = transaksi.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaksi, field, value)
    
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi


@router.delete("/{transaksi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaksi(
    transaksi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not db_transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    
    db.delete(db_transaksi)
    db.commit()
    return None
