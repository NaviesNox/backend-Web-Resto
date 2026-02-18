from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class KategoriMenu(Base):
    __tablename__ = "kategori_menu"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, unique=True, nullable=False)
    deskripsi = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    menu = relationship("Menu", back_populates="kategori")
