from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.karyawan import Karyawan
from app.models.user import User, UserRole
from app.schemas.karyawan import KaryawanCreate, KaryawanUpdate, KaryawanResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/karyawan", tags=["Karyawan"])


@router.get("/", response_model=List[KaryawanResponse])
async def get_karyawan(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    karyawan = db.query(Karyawan).offset(skip).limit(limit).all()
    return karyawan


@router.get("/{karyawan_id}", response_model=KaryawanResponse)
async def get_karyawan_by_id(
    karyawan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    karyawan = db.query(Karyawan).filter(Karyawan.id == karyawan_id).first()
    if not karyawan:
        raise HTTPException(status_code=404, detail="Karyawan not found")
    return karyawan


@router.post("/", response_model=KaryawanResponse, status_code=status.HTTP_201_CREATED)
async def create_karyawan(
    karyawan: KaryawanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_karyawan = Karyawan(**karyawan.model_dump())
    db.add(db_karyawan)
    db.commit()
    db.refresh(db_karyawan)
    return db_karyawan


@router.put("/{karyawan_id}", response_model=KaryawanResponse)
async def update_karyawan(
    karyawan_id: int,
    karyawan: KaryawanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_karyawan = db.query(Karyawan).filter(Karyawan.id == karyawan_id).first()
    if not db_karyawan:
        raise HTTPException(status_code=404, detail="Karyawan not found")
    
    update_data = karyawan.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_karyawan, field, value)
    
    db.commit()
    db.refresh(db_karyawan)
    return db_karyawan


@router.delete("/{karyawan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_karyawan(
    karyawan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_karyawan = db.query(Karyawan).filter(Karyawan.id == karyawan_id).first()
    if not db_karyawan:
        raise HTTPException(status_code=404, detail="Karyawan not found")
    
    db.delete(db_karyawan)
    db.commit()
    return None
