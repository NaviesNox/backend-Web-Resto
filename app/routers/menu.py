from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.menu import Menu
from app.models.user import User, UserRole
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from app.auth import check_role_permission

router = APIRouter(prefix="/api/menu", tags=["Menu"])


@router.get("/", response_model=List[MenuResponse])
async def get_menu(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    menu = db.query(Menu).offset(skip).limit(limit).all()
    return menu


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu_by_id(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN, UserRole.MANAGER]))
):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    update_data = menu.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_menu, field, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_permission([UserRole.ADMIN]))
):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    db.delete(db_menu)
    db.commit()
    return None
