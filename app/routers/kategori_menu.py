from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.kategori_menu import KategoriMenu
from app.models.user import User, UserRole
from app.schemas.kategori_menu import KategoriMenuCreate, KategoriMenuUpdate, KategoriMenuResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/kategori-menu", tags=["Kategori Menu"])


@router.get("/", response_model=List[KategoriMenuResponse])
async def get_kategori_menu(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    kategori = db.query(KategoriMenu).offset(skip).limit(limit).all()
    return kategori


@router.get("/{kategori_id}", response_model=KategoriMenuResponse)
async def get_kategori_menu_by_id(
    kategori_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    kategori = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_id).first()
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori not found")
    return kategori


@router.post("/", response_model=KategoriMenuResponse, status_code=status.HTTP_201_CREATED)
async def create_kategori_menu(
    kategori: KategoriMenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_kategori = KategoriMenu(**kategori.model_dump())
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori


@router.put("/{kategori_id}", response_model=KategoriMenuResponse)
async def update_kategori_menu(
    kategori_id: int,
    kategori: KategoriMenuUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_kategori = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_id).first()
    if not db_kategori:
        raise HTTPException(status_code=404, detail="Kategori not found")
    
    update_data = kategori.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_kategori, field, value)
    
    db.commit()
    db.refresh(db_kategori)
    return db_kategori


@router.delete("/{kategori_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategori_menu(
    kategori_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_kategori = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_id).first()
    if not db_kategori:
        raise HTTPException(status_code=404, detail="Kategori not found")
    
    db.delete(db_kategori)
    db.commit()
    return None
