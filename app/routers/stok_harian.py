from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.stok_harian import StokHarian
from app.models.user import User, UserRole
from app.schemas.stok_harian import StokHarianCreate, StokHarianUpdate, StokHarianResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/stok-harian", tags=["Stok Harian"])


@router.get("/", response_model=List[StokHarianResponse])
async def get_stok_harian(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    stok = db.query(StokHarian).offset(skip).limit(limit).all()
    return stok


@router.get("/{stok_id}", response_model=StokHarianResponse)
async def get_stok_harian_by_id(
    stok_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    stok = db.query(StokHarian).filter(StokHarian.id == stok_id).first()
    if not stok:
        raise HTTPException(status_code=404, detail="Stok Harian not found")
    return stok


@router.post("/", response_model=StokHarianResponse, status_code=status.HTTP_201_CREATED)
async def create_stok_harian(
    stok: StokHarianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    db_stok = StokHarian(**stok.model_dump())
    db.add(db_stok)
    db.commit()
    db.refresh(db_stok)
    return db_stok


@router.put("/{stok_id}", response_model=StokHarianResponse)
async def update_stok_harian(
    stok_id: int,
    stok: StokHarianUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    db_stok = db.query(StokHarian).filter(StokHarian.id == stok_id).first()
    if not db_stok:
        raise HTTPException(status_code=404, detail="Stok Harian not found")
    
    update_data = stok.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_stok, field, value)
    
    db.commit()
    db.refresh(db_stok)
    return db_stok


@router.delete("/{stok_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stok_harian(
    stok_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_stok = db.query(StokHarian).filter(StokHarian.id == stok_id).first()
    if not db_stok:
        raise HTTPException(status_code=404, detail="Stok Harian not found")
    
    db.delete(db_stok)
    db.commit()
    return None
