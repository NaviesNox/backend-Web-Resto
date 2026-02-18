from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.meja import Meja
from app.models.user import User, UserRole
from app.schemas.meja import MejaCreate, MejaUpdate, MejaResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/meja", tags=["Meja"])


@router.get("/", response_model=List[MejaResponse])
async def get_meja(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    meja = db.query(Meja).offset(skip).limit(limit).all()
    return meja


@router.get("/{meja_id}", response_model=MejaResponse)
async def get_meja_by_id(
    meja_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    meja = db.query(Meja).filter(Meja.id == meja_id).first()
    if not meja:
        raise HTTPException(status_code=404, detail="Meja not found")
    return meja


@router.post("/", response_model=MejaResponse, status_code=status.HTTP_201_CREATED)
async def create_meja(
    meja: MejaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    db_meja = Meja(**meja.model_dump())
    db.add(db_meja)
    db.commit()
    db.refresh(db_meja)
    return db_meja


@router.put("/{meja_id}", response_model=MejaResponse)
async def update_meja(
    meja_id: int,
    meja: MejaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER, UserRole.PRAMUSAJI, UserRole.KASIR]))
):
    db_meja = db.query(Meja).filter(Meja.id == meja_id).first()
    if not db_meja:
        raise HTTPException(status_code=404, detail="Meja not found")
    
    update_data = meja.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meja, field, value)
    
    db.commit()
    db.refresh(db_meja)
    return db_meja


@router.delete("/{meja_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meja(
    meja_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_meja = db.query(Meja).filter(Meja.id == meja_id).first()
    if not db_meja:
        raise HTTPException(status_code=404, detail="Meja not found")
    
    db.delete(db_meja)
    db.commit()
    return None
