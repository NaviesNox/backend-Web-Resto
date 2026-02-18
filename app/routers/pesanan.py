from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.pesanan import Pesanan
from app.models.detail_pesanan import DetailPesanan
from app.models.karyawan import Karyawan
from app.models.meja import Meja
from app.models.menu import Menu
from app.models.user import User, UserRole
from app.schemas.pesanan import PesananCreate, PesananUpdate, PesananResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/pesanan", tags=["Pesanan"])


def _pesanan_options():
    return [
        joinedload(Pesanan.meja),
        joinedload(Pesanan.karyawan),
        joinedload(Pesanan.detail_pesanan).joinedload(DetailPesanan.menu),
    ]


@router.get("/", response_model=List[PesananResponse])
async def get_pesanan(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    pesanan = db.query(Pesanan).options(*_pesanan_options()).offset(skip).limit(limit).all()
    return pesanan


@router.get("/{pesanan_id}", response_model=PesananResponse)
async def get_pesanan_by_id(
    pesanan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    pesanan = db.query(Pesanan).options(*_pesanan_options()).filter(Pesanan.id == pesanan_id).first()
    if not pesanan:
        raise HTTPException(status_code=404, detail="Pesanan not found")
    return pesanan


@router.post("/", response_model=PesananResponse, status_code=status.HTTP_201_CREATED)
async def create_pesanan(
    pesanan: PesananCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    # Create pesanan
    db_pesanan = Pesanan(
        meja_id=pesanan.meja_id,
        karyawan_id=pesanan.karyawan_id,
        nama_pelanggan=pesanan.nama_pelanggan,
    )
    db.add(db_pesanan)
    db.commit()
    db.refresh(db_pesanan)
    
    # Create detail pesanan items
    for item in pesanan.items:
        db_detail = DetailPesanan(
            pesanan_id=db_pesanan.id,
            **item.model_dump()
        )
        db.add(db_detail)
    
    db.commit()
    db.refresh(db_pesanan)
    return db_pesanan


@router.put("/{pesanan_id}", response_model=PesananResponse)
async def update_pesanan(
    pesanan_id: int,
    pesanan: PesananUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    db_pesanan = db.query(Pesanan).filter(Pesanan.id == pesanan_id).first()
    if not db_pesanan:
        raise HTTPException(status_code=404, detail="Pesanan not found")
    
    update_data = pesanan.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pesanan, field, value)
    
    db.commit()
    db.refresh(db_pesanan)
    return db_pesanan


@router.delete("/{pesanan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pesanan(
    pesanan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_pesanan = db.query(Pesanan).filter(Pesanan.id == pesanan_id).first()
    if not db_pesanan:
        raise HTTPException(status_code=404, detail="Pesanan not found")
    
    db.delete(db_pesanan)
    db.commit()
    return None
